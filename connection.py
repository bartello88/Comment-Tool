import yaml


def get_database_credentials_from_YAML():
    with open('databaseconfig.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        print(data)
    return data
get_database_credentials_from_YAML()


