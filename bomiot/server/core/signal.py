from django.dispatch import Signal, receiver

test_signal = Signal()


@receiver(test_signal)
def test_signal_callback(sender, **kwargs):
    pass