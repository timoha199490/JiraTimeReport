import os
import configparser


class Credential():
    Login: str
    ApiKey: str
    ServerUrl: str

def init_config():
    credential = Credential()
    if os.path.isfile('./config.ini'):
        read_config(credential)
    else:
        create_config(credential)

    return credential

def read_config(credential: Credential):
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    credential.Login = config['DEFAULT']['Login']
    credential.ApiKey = config['DEFAULT']['ApiKey']
    credential.ServerUrl = config['DEFAULT']['Server']


def create_config(credential: Credential):
    print('Enter jira login(format - user@domain.com):')
    credential.Login = input()
    print('Enter Jira API key(instruction here https://confluence.atlassian.com/cloud/api-tokens-938839638.html):')
    credential.ApiKey = input()
    print('Enter jira URI:')
    credential.ServerUrl = input()

    config = configparser.ConfigParser()
    config['DEFAULT'] = {'Login': credential.Login,
                         'ApiKey': credential.ApiKey,
                         'Server': credential.ServerUrl}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)



