from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import YourModel
from .serializers import YourModelSerializer
from .signal import bomiot_data_signals

class YourModelViewSet(ModelViewSet):
    """
    一个强大的数据库管理和反馈机制的 ViewSet
    """
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer

    def create(self, request, *args, **kwargs):
        """
        重写 create 方法，结合 send_robust 和事务管理
        """
        data = request.data

        try:
            with transaction.atomic():  # 开启事务
                # 发送信号并捕获响应
                responses = bomiot_data_signals.send_robust(sender=self.__class__, data=data)

                # 检查信号处理结果
                for receiver, response in responses:
                    if isinstance(response, Exception):
                        raise response  # 抛出信号处理中的异常
                    if isinstance(response, dict) and response.get("status") == "error":
                        raise ValueError(response.get("message"))

                # 如果信号没有返回错误信息，继续正常的创建流程
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except ValueError as e:
            # 捕获数据验证错误，回滚事务并返回自定义信息
            transaction.set_rollback(True)
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # 捕获其他异常，回滚事务并返回自定义信息
            transaction.set_rollback(True)
            return Response({"status": "error", "message": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)