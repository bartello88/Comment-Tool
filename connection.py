import yaml


def getDatabaseCredentialsFromYAML():
    with open('databaseconfig.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        connection = {}
        connection['database'] = data['config']['database']
        connection['database_dialect'] = data['config']['database_dialect']
        connection['host'] = data['config']['host']
        connection['user'] = data['config']['user']
        connection['password'] = data['config']['password']
        connection['port'] = data['config']['port']
        connection['database_name'] = data['config']['database_name']
        connection['table_name'] = data['config']['table_name']
    return connection
