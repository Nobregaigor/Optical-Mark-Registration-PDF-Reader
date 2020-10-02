from .functions import read_pdf


def get_unumber_from_pdf(*args, **kwargs):
    input_file = args[0]["input_file"]
    data = read_pdf(input_file)
    print(data[0])
