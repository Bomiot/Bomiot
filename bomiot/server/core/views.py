import os
import re

from os.path import join, exists
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser, FormParser
from functools import reduce

from . import serializers, models, filter
from .page import CorePageNumberPagination, PermissionPageNumberPagination, APIPageNumberPagination, TeamPageNumberPagination
from .permission import NormalPermission
from .utils import readable_file_size, sync_write_file
from .signal import bomiot_job_signals
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import MethodNotAllowed
from django_filters.rest_framework import DjangoFilterBackend
from .message import permission_message_return, detail_message_return, msg_message_return, others_message_return

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings
from django.core.cache import cache

User = get_user_model()


class UserPage(CorePageNumberPagination):

    def get_return_data(self, data) -> dict:
        return {"label": data.name, "value": data.id}

    def query_data_add(self) -> list:
        team_list = models.Team.objects.all()
        team_data_list = list(map(lambda data: self.get_return_data(data), team_list))
        department_list = models.Department.objects.all()
        department_data_list = list(map(lambda data: self.get_return_data(data), department_list))
        return [
            ("team", team_data_list),
            ("department", department_data_list)
        ]


class UserList(viewsets.ModelViewSet):
    """
        list:
            Response a user data list（all）
    """
    pagination_class = UserPage
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "username", "created_time", "updated_time", ]
    filter_class = filter.UserFilter

    def get_queryset(self):
        if self.request.user:
            query_data = {'is_delete': False}
            search = self.request.query_params.get('search')
            if search:
                query_data['username__icontains'] = search
            return User.objects.filter(**query_data).order_by('-date_joined')
        else:
            return User.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.UserSerializer
        else:
            raise MethodNotAllowed(self.request.method)
            
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class PermissionList(viewsets.ModelViewSet):
    """
        list:
            Response a permission data list（all）
    """
    pagination_class = PermissionPageNumberPagination
    authentication_classes = []
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.PermissionFilter

    def get_queryset(self):
        if self.request.user:
            return models.Permission.objects.filter().order_by('-id')
        else:
            return models.Permission.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.PermissionSerializer
        else:
            raise MethodNotAllowed(self.request.method)
        
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserCreate(viewsets.ModelViewSet):
    """
        create:
            create a user
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.UserFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.UserSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(username=data.get('username'), is_delete=False)
        if user_check.exists():
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User exists"))
        else:
            if self.request.auth.is_superuser is True:
                User.objects.create_user(username=data.get('username'), password=data.get('username'))
                user_folder = join(settings.MEDIA_ROOT, data.get('username'))
                exists(user_folder) or os.makedirs(user_folder)
            else:
                if "Create One User" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to create user"))
                else:
                    User.objects.create_user(username=data.get('username'), password=data.get('username'))
                    user_folder = join(settings.MEDIA_ROOT, data.get('username'))
                    exists(user_folder) or os.makedirs(user_folder)
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                           "Success Create User"), status=200)


class UserChangePWD(viewsets.ModelViewSet):
    """
        create:
            Change Password
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.UserFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.UserSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(id=data.get('id'), is_delete=False)
        if user_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User not exists"))
        else:
            user_data = user_check.first()
            if self.request.auth.is_superuser is True:
                user_data.set_password(str(data.get('pwd')))
                user_data.save()
            else:
                if "Change Password" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to change password"))
                else:
                    if self.request.auth.id == int(data.get('id')):
                        user_data.set_password(str(data.get('pwd')))
                        user_data.save()
                    else:
                        raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                                 "User can only change your own password"))
            return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                               "Success Change Password"), status=200)


class UserSetTeam(viewsets.ModelViewSet):
    """
        create:
            set team for user
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.UserFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.UserSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(id=int(data.get('id')), is_delete=False)
        if user_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User not exists"))
        else:
            user_data = user_check.first()
            if "Set Team For User" not in self.request.auth.permission:
                raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                         "User does not have permission to set team for user"))
            else:
                team_data = models.Team.objects.filter(id=int(data.get('team_id')), is_delete=False).first()
                user_data.permission = team_data.permission if team_data else {}
                user_data.team = int(data.get('team_id'))
                user_data.save()
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                            "Success set team"), status=200)


class UserSetDepartment(viewsets.ModelViewSet):
    """
        create:
            set department for user
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.UserFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.UserSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(id=data.get('id'), is_delete=False)
        if user_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User not exists"))
        else:
            user_data = user_check.first()
            if "Set Department For User" not in self.request.auth.permission:
                raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                         "User does not have permission to set department for user"))
            else:
                user_data.department = data.get('department_id')
                user_data.save()
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                            "Success set department"), status=200)


class UserLock(viewsets.ModelViewSet):
    """
        create:
            Lock one User
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.UserFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.UserSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(id=data.get('id'), is_delete=False)
        if user_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User not exists"))
        else:
            user_data = user_check.first()
            if user_data.is_superuser:
                raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                         "Can not lock admin"))
            else:
                if "Lock & Unlock User" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to lock user"))
                else:
                    if self.request.auth.id == int(data.get('id')):
                        raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                                 "User can not lock/unlock your own"))
                    else:
                        if user_data.is_active is True:
                            user_data.is_active = False
                            user_data.request_limit = 0
                            user_data.save()
                            return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                               "Success lock User"), status=200)
                        else:
                            user_data.is_active = True
                            user_data.request_limit = 0
                            user_data.save()
                            return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                               "Success unlock User"), status=200)


class UserDelete(viewsets.ModelViewSet):
    """
        create:
            Delete one User
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.UserFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.UserSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        user_check = User.objects.filter(id=data.get('id'), is_delete=False)
        if user_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "User not exists"))
        else:
            user_data = user_check.first()
            if user_data.is_superuser:
                raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                         "Can not delete admin"))
            else:
                if "Delete One User" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to delete user"))
                else:
                    if self.request.auth.id == int(data.get('id')):
                        raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                                 "User can not delete your own"))
                    else:
                        user_data.is_delete = True
                        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                           "Success delete User"), status=200)


class UserUpload(viewsets.ModelViewSet):
    """
        create:
            upload files
    """
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.FileFilter
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        data = self.request.FILES
        exists(join(settings.MEDIA_ROOT, self.request.auth.username)) or os.makedirs(join(settings.MEDIA_ROOT, self.request.auth.username))
        for file_name in data:
            file_obj = self.request.FILES.get(file_name)
            file_extension = file_obj.name.split('.')[-1].lower()
            if file_extension not in settings.FILE_EXTENSION:
                detail = others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "File type not allowed")
                context = {'detail': f"{detail} {file_obj.name}"}
                raise APIException(context)
            if file_obj.size <= settings.FILE_SIZE:
                file_data = file_obj.read()
                file_path = join(settings.MEDIA_ROOT, str(self.request.auth.username), file_obj.name)
                bomiot_job_signals.send(
                    sender=sync_write_file,
                    msg={'models': 'Function'},
                    file_path=file_path,
                    file_data=file_data
                )
                with open(file_path, 'wb') as f:
                    f.write(file_data)
                f.close()
                context = {}
                msg = others_message_return(self.request.META.get('HTTP_LANGUAGE', ''), "Success upload files")
                context['msg'] = f"{msg} {file_obj.name}"
                return Response(context, status=200)
            else:
                file_size = readable_file_size(file_obj.size)
                file_size_limit = readable_file_size(settings.FILE_SIZE)
                detail = others_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                         "File size exceeds limit")
                context['detail'] = f"{detail} {file_size}/{file_size_limit}"
                raise APIException(context)


class FilePage(CorePageNumberPagination):

    def get_user_return_data(self, data):
        return {"label": data.username, "value": data.id}

    def query_data_add(self) -> list:
        user_list = User.objects.filter(is_delete=False).exclude(id=self.request.auth.id)
        user_data_list = list(map(lambda data: self.get_user_return_data(data), user_list))

        return [
            ("users", user_data_list)
        ]


class UserFiles(viewsets.ModelViewSet):
    """
        list:
            Response a user file list（all）
    """
    pagination_class = FilePage
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.FileFilter

    def get_queryset(self):
        if self.request.user:
            query_data = {'is_delete': False}
            search = self.request.query_params.get('search')
            if search:
                query_data['name__icontains'] = search
            if self.request.auth.is_superuser is True:
                return models.Files.objects.filter(**query_data).order_by('-updated_time')
            else:
                share_user = '<->' + str(self.request.auth.id) + "<->" + self.request.auth.username
                return models.Files.objects.filter(
                                            Q(owner=self.request.auth.username, **query_data)
                                            |
                                            Q(shared_to__icontains=share_user, **query_data)
                                            ).order_by('-updated_time')
        else:
            return models.Files.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.FileSerializer
        else:
            raise MethodNotAllowed(self.request.method)
                
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FileShare(viewsets.ModelViewSet):
    """
        create:
            Share your file
    """
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.FileFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.FileSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def get_users_data(self, data):
        user_data = User.objects.filter(id=data).first()
        return "<->" + str(data) + "<->" + user_data.username

    def create(self, request, **kwargs):
        data = self.request.data
        file_check = models.Files.objects.filter(id=data.get('id'), is_delete=False)
        if file_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "File not exists"))
        else:
            file_data = file_check.first()
            if file_data.owner != self.request.auth.username:
                raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                         "Can not share file which is not your own"))
            else:
                users_list = data.get('users')
                data_list = list(map(lambda data: self.get_users_data(data), users_list))
                shared_to_data = ",".join(data_list)
                file_data.shared_to = shared_to_data
                file_data.save()
            return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                               "Success share your file"), status=200)


class DeleteFile(viewsets.ModelViewSet):
    """
        create:
            Delete one file
    """
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.FileFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.FileSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        file_check = models.Files.objects.filter(id=data.get('id'), is_delete=False)
        if file_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "File not exists"))
        else:
            file_data = file_check.first()
            if self.request.auth.is_superuser is True:
                file_data.is_delete = True
            else:
                if file_data.owner != self.request.auth.username:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "Can not delete file which is not your own"))
                else:
                    file_data.is_delete = True
            file_data.save()
            return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                               "Success delete file"), status=200)


class TeamList(viewsets.ModelViewSet):
    """
        list:
            Response a team data list（all）
    """
    pagination_class = TeamPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "name", "created_time", "updated_time", ]
    filter_class = filter.TeamFilter

    def get_queryset(self):
        if self.request.user:
            query_data = {'is_delete': False}
            search = self.request.query_params.get('search')
            if search:
                query_data['name__icontains'] = search
            return models.Team.objects.filter(**query_data).order_by('-id')
        else:
            return models.Team.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.TeamSerializer
        else:
            raise MethodNotAllowed(self.request.method)
            
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TeamCreate(viewsets.ModelViewSet):
    """
        create:
            create a team
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.TeamFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.TeamSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        team_check = models.Team.objects.filter(name=data.get('name'), is_delete=False)
        if team_check.exists():
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "Team exists"))
        else:
            if self.request.auth.is_superuser is True:
                models.Team.objects.create(name=data.get('name'))
            else:
                if "Create One Team" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to create team"))
                else:
                    models.Team.objects.create(name=data.get('name'))
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                           "Success create team"), status=200)


class TeamPermission(viewsets.ModelViewSet):
    """
        create:
            Set permission for team
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.TeamFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.TeamSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def get_permission_data(self, data):
        permission_data = models.Permission.objects.filter(name=data).first()
        return {
            permission_data.name: permission_data.api
        }

    def create(self, request, **kwargs):
        data = self.request.data
        team_check = models.Team.objects.filter(id=data.get('id'), is_delete=False)
        if team_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "Team not exists"))
        else:
            team_data = team_check.first()
            if "Set Permission For Team" not in self.request.auth.permission:
                raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                         "User does not have permission to set permission for team"))
            else:
                permission_list = data.get('permission')
                data_list = list(map(lambda data: self.get_permission_data(data), permission_list))
                permission_data = reduce(lambda x, y: {**x, **y}, data_list)
                team_data.permission = permission_data
                User.objects.filter(team=team_data.id, is_delete=False).update(
                    permission=permission_data
                )
                team_data.save()
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                            "Success change team permission"), status=200)


class TeamChange(viewsets.ModelViewSet):
    """
        create:
            Change one team
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.TeamFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.TeamSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        team_check = models.Team.objects.filter(name=data.get('name'), is_delete=False)
        if team_check.exists():
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "Team exists"))
        else:
            if self.request.auth.is_superuser is True:
                models.Team.objects.filter(id=data.get('id')).update(name=data.get('name'))
            else:
                if "Change Team" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to change team"))
                else:
                    models.Team.objects.filter(id=data.get('id')).update(name=data.get('name'))
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                           "Success change team"), status=200)


class TeamDelete(viewsets.ModelViewSet):
    """
        create:
            Delete one team
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.TeamFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.TeamSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        team_check = models.Team.objects.filter(id=data.get('id'), is_delete=False)
        if team_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "Team not exists"))
        else:
            if self.request.auth.is_superuser is True:
                models.Team.objects.filter(id=data.get('id')).update(is_delete=True)
            else:
                if "Delete Team" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to delete team"))
                else:
                    models.Team.objects.filter(id=data.get('id')).update(is_delete=True)
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                           "Success delete team"), status=200)


class DepartmentList(viewsets.ModelViewSet):
    """
        list:
            Response a department data list（all）
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "name", "created_time", "updated_time", ]
    filter_class = filter.DepartmentFilter

    def get_queryset(self):
        if self.request.user:
            query_data = {'is_delete': False}
            search = self.request.query_params.get('search')
            if search:
                query_data['name__icontains'] = search
            return models.Department.objects.filter(**query_data).order_by('-id')
        else:
            return models.Department.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.DepartmentSerializer
        else:
            raise MethodNotAllowed(self.request.method)
            
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class DepartmentCreate(viewsets.ModelViewSet):
    """
        create:
            create one department
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.DepartmentFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.DepartmentSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        department_check = models.Department.objects.filter(name=data.get('name'), is_delete=False)
        if department_check.exists():
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "Department exists"))
        else:
            if self.request.auth.is_superuser is True:
                models.Department.objects.create(name=data.get('name'))
            else:
                if "Create department" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to create department"))
                else:
                    models.Department.objects.create(name=data.get('name'))
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                           "Success create department"), status=200)


class DepartmentChange(viewsets.ModelViewSet):
    """
        create:
            Change one department
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.DepartmentFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.DepartmentSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        department_check = models.Department.objects.filter(name=data.get('name'), is_delete=False)
        if department_check.exists():
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "Department exists"))
        else:
            if self.request.auth.is_superuser is True:
                models.Department.objects.filter(id=data.get('id')).update(name=data.get('name'))
            else:
                if "Change department" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to change department"))
                else:
                    models.Department.objects.filter(id=data.get('id')).update(name=data.get('name'))
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                           "Success change department"), status=200)


class DepartmentDelete(viewsets.ModelViewSet):
    """
        create:
            Delete one department
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.DepartmentFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.DepartmentSerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        department_check = models.Department.objects.filter(id=data.get('id'), is_delete=False)
        if department_check.exists() is False:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "Department not exists"))
        else:
            if self.request.auth.is_superuser is True:
                models.Department.objects.filter(id=data.get('id')).update(is_delete=True)
            else:
                if "Delete department" not in self.request.auth.permission:
                    raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to delete department"))
                else:
                    models.Department.objects.filter(id=data.get('id')).update(is_delete=True)
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                           "Success delete department"), status=200)


class APIList(viewsets.ModelViewSet):
    """
        list:
            Response a api data list（all）
    """
    pagination_class = APIPageNumberPagination
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "api", "func_name", "created_time", "updated_time", ]
    filter_class = filter.APIFilter

    def get_queryset(self):
        if self.request.user:
            query_data = {'is_delete': False}
            search = self.request.query_params.get('search')
            if search:
                query_data['api__icontains'] = search
            return models.API.objects.filter(**query_data).order_by('id')
        else:
            return models.API.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.APISerializer
        else:
            raise MethodNotAllowed(self.request.method)
            
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class APIChange(viewsets.ModelViewSet):
    """
        create:
            Change one API
    """
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = filter.APIFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.APISerializer
        else:
            raise MethodNotAllowed(self.request.method)

    def create(self, request, **kwargs):
        data = self.request.data
        data_check = bool(re.search(r'\s', data))
        if data_check is True:
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "API name can not contain space"))
        department_check = models.API.objects.filter(func_name=data.get('func_name'), is_delete=False)
        if department_check.exists():
            raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                     "API exists"))
        else:
            
            if self.request.auth.is_superuser is True:
                models.API.objects.filter(id=data.get('id')).update(func_name=data.get('func_name'))
            else:
                raise APIException(detail_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                                             "User does not have permission to change API"))
        return Response(msg_message_return(self.request.META.get('HTTP_LANGUAGE', ''),
                                           "Success change API"), status=200)


class PyPiList(viewsets.ModelViewSet):
    """
        list:
            Response a PyPi data list（all）
    """
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ["id", "created_time", "updated_time", ]
    filter_class = filter.PyPiFilter

    def get_queryset(self):
        if self.request.user:
            query_data = {}
            query_data['is_delete'] = False
            query_data['category__icontains'] = self.request.query_params.get('search')
            return models.PyPi.objects.filter(**query_data).order_by('-date')
        else:
            return models.PyPi.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.PyPiSerializer
        else:
            raise MethodNotAllowed(self.request.method)
        
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PyPiChartsPage(CorePageNumberPagination):
    def __init__(self, *args, **kwargs):
        self.pypi_data = {}
        self.pypi_data['title'] = 'Bomiot PyPi Downloads Pie Chart'
        self.pypi_data['xAxis_list'] = []
        self.with_mirrors_list = []
        self.without_mirrors_list = []
        super(PyPiChartsPage, self).__init__(*args, **kwargs)
    
    def get_pypi_return_data(self, data) -> dict:
        date_check = data.date.strftime("%m-%d")
        if date_check in self.pypi_data['xAxis_list']:
            return data
        else:
            self.pypi_data['xAxis_list'].append(date_check)
            with_mirrors_check =  models.PyPi.objects.filter(category='with_mirrors', date=data.date)
            without_mirrors_check =  models.PyPi.objects.filter(category='without_mirrors', date=data.date)
            if with_mirrors_check.exists():
                self.with_mirrors_list.append(with_mirrors_check.first().downloads)
            else:
                self.with_mirrors_list.append(0)
            if without_mirrors_check.exists():
                self.without_mirrors_list.append(without_mirrors_check.first().downloads)
            else:
                self.without_mirrors_list.append(0)
        return data

    def query_data_add(self) -> list:
        pypi_list = models.PyPi.objects.filter().order_by('-date')[:90]
        pypi_data_list = list(map(lambda data: self.get_pypi_return_data(data), pypi_list))

        self.pypi_data['xAxis_list'] = list(reversed(self.pypi_data['xAxis_list']))
        self.pypi_data['series_list'] = [
            { 'name': "with_mirrors", 'data': list(reversed(self.with_mirrors_list)) },
            { 'name': "without_mirrors", 'data': list(reversed(self.without_mirrors_list)) }
        ]

        return [
            ("pypi_data", self.pypi_data),
        ]


class PyPiCharts(viewsets.ModelViewSet):
    """
        list:
            Response a PID Charts data list（all）
    """
    pagination_class = PyPiChartsPage
    permission_classes = [NormalPermission, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ["id", "created_time", "updated_time", ]
    filter_class = filter.PyPiFilter

    def get_queryset(self):
        return models.PyPi.objects.none()

    def get_serializer_class(self):
        if self.action in ['list']:
            return serializers.PyPiSerializer
        else:
            raise MethodNotAllowed(self.request.method)
        
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

