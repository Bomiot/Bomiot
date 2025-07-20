# Function Data

## 介绍

- **Bomiot** 的自带API是核心功能，提供了一套全新的前后端交互
- 前后端data数据交互会全部传输到`receiver.py`中
- 通过`receiver.py`做数据接管，从而达到自由开发的交互目的

---

## 数据交互文件

- 使用命令 `bomiot project <your_project>` 后，你会得到一个文件结构

```shell
your-project/                  # 项目目录
├── media/                     # 静态文件
│   ├── img/                   # 公用图片       
│   └── ***.md                 # md的各种文档
├── __version__.py             # your_project版本
├── bomiotconf.ini             # Bomiot项目标识文件
└── receiver.py                # 数据中心
setup.ini                      # 项目配置文件
...

```

---

## 示例`receiver.py`

```python
class ExampleClass(object):

    def example_get(self, data):
        print(data.get('query_params').get('params'))
        example_list = Example.objects.filter()
        qs_list = queryset_to_dict(example_list)
        return [
            ('results', data.get('data')),
        ]

    def example_create(self, data):
        print(data.get('data'))
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        return msg_message_return(language, "Success Create")
    
    def example_update(self, data):
        print(data.get('data'))
        print(data.get('updated_fields'))
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        return msg_message_return(language, "Success Update")
    
    def example_delete(self, data):
        print(data.get('data'))
        language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
        return msg_message_return(language, "Success Delete")
```

---

## `GET`

- **Bomiot** 认为，前端往后端发送Json，后端就应该Json存储
- 后端如果字段再一一对应，是低效且影响开发进度的

```python
def example_get(self, data):
    print(data.get('query_params').get('params'))
    example_list = Example.objects.filter()
    qs_list = queryset_to_dict(example_list)
    return [
        ('results', data.get('data')),
    ]
```

- 我们展开这个`example_list`，来看下他是什么样子的

```json
[{
    id: 1,
    data: {
        name: "test1",
        type: 1
    },
    is_delete: False,
    created_time: datetime,
    updated_time: datetime,
}]
```

- 所以我们需要使用`queryset_to_dict`序列化一下

```json
[{
    id: 1,
    name: "test1",
    type: 1,
    is_delete: False,
    created_time: datetime,
    updated_time: datetime,
}]
```

- 一般情况下，我们不需要接管Get请求
- 在我们需要往前端api中添加新数据的时候，我们才会接口接管

```python
return [
        ('results', data.get('data')),  # 这是默认值，可以直接return自己新添加的数据
    ]
```

`注意:`

- `return` 的是元组

---

## `Create`

```python
def example_create(self, data):
    print(data.get('data'))
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success Create")
```

- 创建数据的接口接管，必须返回交互结果
- 如果不接管创建数据接口，默认就是前端传什么，后端存什么
- 一共3种返回端口

```python
from bomiot_message import msg_message_return, detail_message_return, login_message_return
```

`注意:`

- 只有`msg_message_return`的时候，**Bomiot** 才会存储数据，并且前端提示成功
- `detail_message_return`的时候，前端返回不能存储的反馈信息
- `login_message_return`的时候，会触发前端重新登入，并且数据不会呗存储

---

## `Update`

```python
def example_update(self, data):
    print(data.get('data'))
    print(data.get('updated_fields'))
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success Update")
```

- 更新数据与创建数据不同的是，**Bomiot** 会告诉你更新了哪些字段 `data.get('updated_fields')`
- 其他机制与创建数据是一样的

---

## `Delete`

```python
def example_delete(self, data):
    print(data.get('data'))
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success Delete")
```

- 机制与创建数据是一样的

---

## 自定义

- 用户可以通过models中的`API`自定义api字段
- **Bomiot** 会自动到`receiver.py`中寻找你的自定义字段
- `views.py` 可以参考`example.py` 进行修改

---

## `注意`

- **Bomiot** 的信号机制是热更新，就是，他是即时生效的，无需重启服务器
- 数据接管后，指向其他文件做调用，避免`receiver.py`过于臃肿