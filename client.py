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
