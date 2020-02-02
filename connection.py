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
        connection['databasename'] = data['config']['databasename']
        connection['table_name'] = data['config']['table']
    return connection
