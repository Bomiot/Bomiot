from pathlib import Path
from threading import Thread, Timer
from django.conf import settings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
from bomiot.server.core.models import Files
from .utils import readable_file_size
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from .utils import compare_dicts
from .signal import bomiot_signals

User = get_user_model()


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        self.timer = None
        self.snapshot = DirectorySnapshot(settings.MEDIA_ROOT)

    def on_any_event(self, event):
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(0.2, self.check_snapshot)
        self.timer.start()

    def check_snapshot(self):
        snapshot = DirectorySnapshot(settings.MEDIA_ROOT)
        diff = DirectorySnapshotDiff(self.snapshot, snapshot)
        self.snapshot = snapshot
        self.timer = None

        created_file_list = list(map(lambda data: self.created_file(data), diff.files_created))
        modified_file_list = list(map(lambda data: self.modified_file(data), diff.files_modified))
        deleted_file_list = list(map(lambda data: self.deleted_file(data), diff.files_deleted))
        moved_file_list = list(map(lambda data: self.moved_file(data), diff.files_moved))

    def created_file(self, data):
        detail = Path(data)
        user_check = User.objects.filter(username=detail.parent.name)
        if user_check.exists():
            file_data = Files.objects.create(
                        name=detail.name,
                        type=detail.name.split('.')[-1].lower(),
                        size=readable_file_size(detail.stat().st_size),
                        owner=detail.parent.name
                    )
            bomiot_signals.send(msg={
                'models': 'Files',
                'type': 'create',
                'data': {
                    'id': file_data.id,
                    'name': file_data.name,
                    'type': file_data.type,
                    'size': file_data.size,
                    'owner': file_data.owner,
                    'shared_to': file_data.shared_to
                }
            })


    def modified_file(self, data):
        detail = Path(data)
        user_check = User.objects.filter(username=detail.parent.name)
        if user_check.exists():
            file_data_check = Files.objects.filter(name=detail.name, owner=detail.parent.name)
            if file_data_check.exists():
                old_instance = file_data_check.first()
                new_instance = Files.objects.filter(name=detail.name, owner=detail.parent.name).first()
                new_instance.size=readable_file_size(detail.stat().st_size)
                new_instance.is_delete = False
                new_instance.save()
                instance = Files.objects.filter(id=old_instance.id).first()
                data_before_update = model_to_dict(old_instance)
                data_after_update = model_to_dict(instance)
                data_before_update['created_time'] = old_instance.created_time
                data_after_update['created_time'] = instance.created_time
                data_before_update['updated_time'] = old_instance.updated_time
                data_after_update['updated_time'] = instance.updated_time
                updated_fields = compare_dicts(data_before_update, data_after_update)
                bomiot_signals.send(msg={
                    'models': 'Files',
                    'type': 'update',
                    'data': {
                        'id': instance.id,
                        'name': instance.name,
                        'type': instance.type,
                        'size': instance.size,
                        'owner': instance.owner,
                        'shared_to': instance.shared_to
                    },
                    'updated_fields': updated_fields
                })

    def deleted_file(self, data):
        detail = Path(data)
        user_check = User.objects.filter(username=detail.parent.name)
        if user_check.exists():
            Files.objects.filter(name=detail.name, owner=detail.parent.name).delete()

    def moved_file(self, data):
        move_from = Path(data[0])
        move_from_user = User.objects.filter(username=move_from.parent.name)
        if move_from_user.exists():
            Files.objects.filter(name=move_from.name, owner=move_from.parent.name).delete()
        move_to = Path(data[1])
        move_to_user = User.objects.filter(username=move_to.parent.name)
        if move_to_user.exists():
            Files.objects.create(
                name=move_to.name,
                type=move_to.name.split('.')[-1].lower(),
                size=readable_file_size(move_to.stat().st_size),
                owner=move_to.parent.name,
                shared_to=''
            )

observer = Observer()
event_handler = MyHandler()


class ObserverManager(Thread):
    """
        Observer of media folder
    """

    def __init__(self, observer):
        """
        init manager
        :param observer:
        """
        super(ObserverManager, self).__init__()
        self.observer = observer
        self.observer.start()

    def run(self):
        """
        heart beat detect
        :return:
        """
        self.observer.schedule(event_handler, path=settings.MEDIA_ROOT, recursive=True)


# init observer manager
ob = ObserverManager(observer)
