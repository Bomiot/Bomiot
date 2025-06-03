def flatten_json(nested_dict):
    # 直接解包data内容，再覆盖外层字段（性能更高）
    return {
        **nested_dict['data'],  # 展开data子字典内容
        'id': nested_dict['id'],
        'created_time': nested_dict['created_time'],
        'updated_time': nested_dict['updated_time']
    }

# 原始嵌套JSON数据（示例输入）
original_data = {
    "id": 8,
    "data": {
        "value": 123,
        "status": "active",
        "description": "这是一个有效的数据项"
    },
    "created_time": "2025-05-27 06:33:11",
    "updated_time": "2025-05-27 06:33:11"
}

# 执行展平操作
flattened_data = flatten_json(original_data)

# 打印结果（可根据需要调整输出格式）
print("展平后的JSON数据:")
import json
import orjson
print(orjson.dumps(flattened_data).decode())