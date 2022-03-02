import asana
import config

def asana_login(personal_access_token: str):

    config.LOGGER.info("asana_login() - START")

    client = asana.Client.access_token(personal_access_token)
    me = client.users.me()
    workspace = me['workspaces'][0]
    
    config.LOGGER.info("asana_login() - COMPLETED")

    return {'client':client,'workspace':workspace}


