from rest_framework_csv.renderers import CSVStreamingRenderer

def file_headers():
    return [
    ]

def data_header():
    return dict([
    ])


class FileRender(CSVStreamingRenderer):
    header = file_headers()
    labels = data_header()
