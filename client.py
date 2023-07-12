# The main idea is to create a 'connector.txt' file, then send and receive data
# from it. Easy communication, but it has some disadvantages, e.g. safety. But
# as I use this program only for myself, it is not such a big problem. The
# functions' names are speaking for itself what they are doing, so I will not
# bring any explanations with documentation

import os

def get_connector_path():
    root_folder = r"/"
    target_file = 'connector.txt'
    for root, dirs, files in os.walk(root_folder):
        if target_file in files:
            file_path = os.path.join(root, target_file)
            return file_path

def read_from_file(file_path):
    with open(file_path, 'r') as file:
        message = file.read()
        if message.find('server') != -1:
            print(message)
            return message.replace('server', '').replace('\n', '')
        else:
            return ''

def load_to_file(file_path, message):
    with open(file_path, 'w') as file:
        file.truncate(0)
        print('client\n' + message)
        file.write('client\n' + message)
