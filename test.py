from textwrap import indent

import polars as pd
import orjson, json
from datetime import datetime
import time
start_time = time.time()

#Time taken: 0.008945465087890625 seconds
# 读取Excel文件
df = pd.read_excel('办公用品库.xlsx', sheet_id=1)
# print(df.to_dict(as_series=True))
# for i in df.to_dict(as_series=False):
#     print(df.to_dict(as_series=False)[i])


# def datetime_serializer(obj):
#     if isinstance(obj, datetime):
#         return obj.isoformat()
#     raise TypeError

# 使用orjson将DataFrame转换为JSON字符串
# json_str = orjson.dumps(df.to_dict(as_series=False), ensure_ascii=False)
# print(json_str)
# with open('data.json', 'wb') as f:
#     f.write(json_str)
# data = orjson.loads(json_str)
# print(json_str)
#
# with open('data.json', 'w') as f:
#     json.dump(data, f, indent=4, ensure_ascii=False)
# print(len(data[1:10]))
# for i in data:
#     print(i)
#
# print(len(data))

end_time = time.time()
print(f'Result: Time taken: {end_time - start_time} seconds')

# Result: Time taken: 0.028983592987060547 seconds