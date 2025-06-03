from bomiot.server.core.utils import msg_message_return
from bomiot.server.core.models import Example
from bomiot.server.core.utils import queryset_to_dict


# class ExampleClass:
    # def example_get(self, data):
    #     print(data.get('query_params').get('params'))
    #     example_list = Example.objects.filter()
    #     qs_list = queryset_to_dict(example_list)
    #     return [
    #         ('results', data.get('data')),
    #     ]

    # def example_create(self, data):
    #     print(data.get('data'))
    #     language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    #     return msg_message_return(language, "Success Create")
    
    # def example_update(self, data):
    #     print(data.get('data'))
    #     print(data.get('updated_fields'))
    #     language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    #     return msg_message_return(language, "Success Update")
    
    # def example_delete(self, data):
    #     print(data.get('data'))
    #     language = data.get('request').META.get('HTTP_LANGUAGE', 'en-US')
    #     return msg_message_return(language, "Success Delete")