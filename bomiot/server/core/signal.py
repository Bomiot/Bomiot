from django.dispatch import Signal, receiver
import importlib
import inspect
from .utils import sync_write_file

class BomiotSignal(Signal):
    """
    Custom Signal class, using 'Bomiot' as the default sender
    """

    def _send_signal(self, robust=False, **kwargs):
        """
        Internal method for sending signals.
        :param robust: Whether to use the send_robust method
        :param kwargs: Signal parameters
        """
        msg = kwargs.get('msg', '')
        sender = 'Bomiot'
        if robust:
            return super().send_robust(sender=sender, msg=msg)
        return super().send(sender=sender, msg=msg)

    def send(self, **kwargs):
        """
        Override the default send method, using 'Bomiot' as the sender
        """
        return self._send_signal(robust=False, **kwargs)

    def send_robust(self, **kwargs):
        """
        Override the default send_robust method, using 'Bomiot' as the sender
        """
        return self._send_signal(robust=True, **kwargs)


# Instantiate the custom signal
bomiot_signals = BomiotSignal()
bomiot_job_signals = Signal()
bomiot_data_signals = Signal()

@receiver(bomiot_job_signals)
def bomiot_signal_callback(sender, **kwargs):
    """
    Signal receiver to handle the received job signal
    """
    if kwargs.get('msg', '').get('models', '') == 'Function':
        if sender == sync_write_file:
            sync_write_file(
                kwargs.get('file_path'),
                kwargs.get('file_data')
            )
        else:
            job_func = importlib.import_module(f'{sender.__module__}')
            job_function = getattr(job_func, sender.__name__)
            sig = inspect.signature(job_function)
            if sig.parameters:
                func_kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}
                job_function(**func_kwargs)
            else:
                job_function()