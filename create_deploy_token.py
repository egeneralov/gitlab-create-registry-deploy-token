from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import urllib

def find_csrf_token(text):
  soup = BeautifulSoup(text, "lxml")
  return {
    soup.find(attrs={"name": "csrf-param"}).get("content"): soup.find(attrs={"name": "csrf-token"}).get("content")
  }


def sign_in(session, url, login, password):
  data = {
    "user[login]": login,
    "user[password]": password,
    "user[remember_me]": 0,
    "utf8": "✓"
  }
  r = session.get(url)
  data.update(
    find_csrf_token(r.text)
  )
  return session.post(
    url,
    data = data
  )


def create_token(session, url, suffix, name):
  data = {
    'deploy_token[name]': name,
#     'deploy_token[expires_at]': '',
    'deploy_token[read_repository]': '0',
#     'deploy_token[read_registry]': "0",
    'deploy_token[read_registry]': "1",
  }
  r = session.get(url)
#   print(find_csrf_token(r.text))
  data.update(
    find_csrf_token(r.text)
  )
  return session.post(
    url + suffix,
#     params = data,
    data = data

    # urllib.urlencode('utf8=✓&deploy_token[name]=k8s&deploy_token[expires_at]=&deploy_token[read_repository]=0&deploy_token[read_registry]=0&deploy_token[read_registry]=1&authenticity_token=' + find_csrf_token(r.text)["authenticity_token"])
  )


def main(config):
  session = requests.Session()
  r = sign_in(
    session,
    '{uri.scheme}://{uri.netloc}/users/sign_in'.format(uri=urlparse(config["url"])),
    config['username'],
    config['password']
  )
  try:
    r = create_token(
      session,
      config['url'],
      'settings/repository/deploy_token/create',
      config['name']
    )
  except Exception as err:
    print(err)
    raise Exception('Login failed')
  soup = BeautifulSoup(r.text, "lxml")
  try:
    return {
      "username": soup.find(id="deploy-token-user").get("value"),
      "token": soup.find(id="deploy-token").get("value")
    }
  except Exception as err:
    print(err)
    raise Exception('Token create failed')
  raise Exception("What's happend?")


