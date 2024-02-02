def read_from_file(file_name):
    with open(file_name, 'r') as text:
        text = text.read()
    return text
