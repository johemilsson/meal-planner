import os
import yaml
from ticktick.oauth2 import OAuth2        # OAuth2 Manager
from ticktick.api import TickTickClient   # Main Interface

from src import ROOT_DIR


credentials_file = os.path.join(ROOT_DIR, ".credentials")
with open(credentials_file, "r") as fid:
    credentials = yaml.safe_load(fid)

auth_client = OAuth2(client_id=credentials["client-id"],
                     client_secret=credentials["client-secret"],
                     redirect_uri="http://127.0.0.1:8080")

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0"
X_DEVICE_ = '{"platform":"web","os":"OS X","device":"Firefox 123.0","name":"unofficial api!","version":4531,' \


def new_login(self, username, password):
    url = self.BASE_URL + 'user/signon'
    user_info = {
        'username': username,
        'password': password,
    }
    parameters = {
        'wc': True,
        'remember': True
    }

    response = self.http_post(url, json=user_info, params=parameters, headers=self.HEADERS)
    self.access_token = response['token']
    self.cookies['t'] = self.access_token

TickTickClient._login = new_login

def get_client():
    client = TickTickClient(
        username=credentials["username"],
        password=credentials["password"],
        oauth=auth_client,
    )

    return client