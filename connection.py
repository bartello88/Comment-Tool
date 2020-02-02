import yaml
def getDatabaseCredentials():
    with open('databaseconfig.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        connection ={}
        connection['database'] = data['mysql']['database']
        connection['host'] = data['mysql']['host']
        connection['user'] = data['mysql']['user']
        connection['password'] = data['mysql']['password']
        connection['port'] = data['mysql']['port']
        connection['databasename'] = data['mysql']['databasename']
    return connection