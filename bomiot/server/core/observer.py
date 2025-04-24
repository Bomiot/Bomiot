from pathlib import Path
from threading import Thread, Timer
from django.conf import settings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
from bomiot.server.core.models import Files
from .utils import readable_file_size
from django.contrib.auth import get_user_model

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
            Files.objects.create(
                name=detail.name,
                type=detail.name.split('.')[-1].lower(),
                size=readable_file_size(detail.stat().st_size),
                owner=detail.parent.name
            )


    def modified_file(self, data):
        detail = Path(data)
        user_check = User.objects.filter(username=detail.parent.name)
        if user_check.exists():
            Files.objects.filter(name=detail.name, owner=detail.parent.name).update(
                size=readable_file_size(detail.stat().st_size),
            )

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
