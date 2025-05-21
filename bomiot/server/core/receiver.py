from django.dispatch import receiver
from .signal import bomiot_data_signals

@receiver(bomiot_data_signals)
def handle_data_signal(sender, **kwargs):
    """
    处理信号数据，验证数据是否符合要求。
    """
    data = kwargs.get('data')
    if not data or not isinstance(data, dict):
        raise ValueError("Invalid data format: data must be a dictionary.")

    # 验证数据是否包含必需字段
    required_fields = ['name', 'description']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # 如果数据符合要求，返回成功信息
    return {"status": "success", "message": "Data is valid."}