"""Reading config data or creating in. Author timoha199490@gmail.com"""
import os
import configparser


class Credential():
    login: str
    api_key: str
    server_url: str

    def __init__(self):
        """Constructor"""
        pass

def init_config():
    """Main method for configuration reading/creating"""
    credential = Credential()
    if os.path.isfile('./config.ini'):
        read_config(credential)
    else:
        _create_config(credential)

    return credential

def read_config(credential: Credential):
    """Read configuration from ini file"""
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    credential.login = config['DEFAULT']['Login']
    credential.api_key = config['DEFAULT']['ApiKey']
    credential.server_url = config['DEFAULT']['Server']


def _create_config(credential: Credential):
    """If ini config doesn't exist creating it"""
    print('Enter jira login(format - user@domain.com):')
    credential.login = input()
    print('Enter Jira API key(instruction here '
          'https://confluence.atlassian.com/cloud/api-tokens-938839638.html):')
    credential.api_key = input()
    print('Enter jira URI:')
    credential.server_url = input()

    config = configparser.ConfigParser()
    config['DEFAULT'] = {'Login': credential.login,
                         'ApiKey': credential.api_key,
                         'Server': credential.server_url}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
