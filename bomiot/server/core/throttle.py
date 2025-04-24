from rest_framework.throttling import BaseThrottle
from .models import ThrottleModel
from django.utils import timezone
from django.conf import settings

data = {}


class CoreThrottle(BaseThrottle):
    def allow_request(self, request, view) -> bool:
        ip = request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get(
            'HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
        now_time = timezone.now()
        cur_time = now_time - timezone.timedelta(seconds=1)
        throttle_cur_time_list = ThrottleModel.objects.filter(method=request.method.lower(), created_time__lte=cur_time)
        for i in throttle_cur_time_list:
            i.delete()
        throttle_allocation_list = ThrottleModel.objects.filter(ip=ip, method=request.method.lower()).order_by('id')
        throttle_count = throttle_allocation_list.count()
        if throttle_count == 0:
            ThrottleModel.objects.create(ip=ip, method=request.method.lower())
            return True
        else:
            throttle_last_created_time = throttle_allocation_list.first().created_time
            ThrottleModel.objects.create(ip=ip, method=request.method.lower())
            allocation_seconds_balance = (now_time - throttle_last_created_time).seconds
            data["visit_check"] = throttle_last_created_time
            if allocation_seconds_balance >= settings.ALLOCATION_SECONDS:
                return True
            else:
                if throttle_count >= settings.THROTTLE_SECONDS:
                    return False
                else:
                    return True

    def wait(self):
        cur_time = timezone.now()
        wait_time = (cur_time - data["visit_check"]).seconds
        balance_time = 1 - wait_time
        return balance_time
