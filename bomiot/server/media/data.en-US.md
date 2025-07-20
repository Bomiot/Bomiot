# Function Data

## Introduction

- **Bomiot**'s built-in API is the core function, providing a new set of front-end and back-end interactions
- All front-end and back-end data interactions will be transferred to `receiver.py`
- Data takeover is done through `receiver.py`, so as to achieve the interactive purpose of free development

---

## Data interaction file

- After using the command `bomiot project <your_project>`, you will get a file structure

```shell
your-project/            # Project directory
├── media/               # Static files
│ ├── img/               # Public images
│ └── ***.md             # Various documents of md
├── __version__.py       # your_project version
├── bomiotconf.ini       # Bomiot project identification file
└── receiver.py          # Data center
setup.ini                # Project configuration file
...

```

---

## Example `receiver.py`

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

- **Bomiot** believes that if the front end sends Json to the back end, the back end should store it in Json
- If the back end has one-to-one correspondence between fields, it is inefficient and affects the development progress

```python
def example_get(self, data):
    print(data.get('query_params').get('params'))
    example_list = Example.objects.filter()
    qs_list = queryset_to_dict(example_list)
    return [
        ('results', data.get('data')),
    ]
```

- Let's expand this `example_list` and see what it looks like

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

- So we need to use `queryset_to_dict` to serialize it

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

- In general, we don't need to take over the Get request
- When we need to add new data to the front-end API, we will take over the interface

```python
return [
    ('results', data.get('data')), # This is the default value, you can directly return the newly added data
]
```

`Note:`

- `return` is a tuple

---

## `Create`

```python
def example_create(self, data):
    print(data.get('data'))
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success Create")
```

- The interface takes over the creation of data, and the interaction result must be returned
- If you do not take over the creation of the data interface, the default is what the front-end transmits and what the back-end stores
- There are 3 return ports in total

```python
from bomiot_message import msg_message_return, detail_message_return, login_message_return
```

`Note:`

- Only when `msg_message_return` occurs, **Bomiot** will store data, and the front-end will prompt success
- When `detail_message_return` occurs, the front-end returns feedback information that cannot be stored
- When `login_message_return` occurs, it will trigger the front-end to log in again, and the data will not be stored

---

## `Update`

```python
def example_update(self, data):
    print(data.get('data'))
    print(data.get('updated_fields'))
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success Update")
```

- The difference between updating data and creating data is that **Bomiot** It will tell you which fields have been updated `data.get('updated_fields')`
- Other mechanisms are the same as creating data

---

## `Delete`

```python
def example_delete(self, data):
    print(data.get('data'))
    language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    return msg_message_return(language, "Success Delete")
```

- The mechanism is the same as creating data

---

## Customization

- Users can customize api fields through `API` in models
- **Bomiot** will automatically look for your custom fields in `receiver.py`
- `views.py` can be modified by referring to `example.py`

---

## `Note`

- **Bomiot**'s signal mechanism is hot update, that is, it takes effect immediately without restarting the server
- After the data is taken over, point to other files for calling to avoid `receiver.py` being too bloated