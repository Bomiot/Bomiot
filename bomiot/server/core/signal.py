from django.dispatch import Signal, receiver

bomiot_signals = Signal()

# @receiver(bomiot_signals)
# def bomiot_signal_callback(sender, **kwargs):
#     print(sender, kwargs)
