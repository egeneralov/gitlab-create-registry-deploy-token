# Gitlab: create registry deploy token

## How to

#### Create json file

    {
      "url": "https://gitlab.com/group/project/",
      "username": "user@domain.tld",
      "password": "password",
      "name": "name-of-deploy-token",
      "read_repository": 0,
      "read_registry": 1
    }

#### Load into script

    curl -s -d@some.json https://gitlab-create-deploy-token.herokuapp.com/ | jq

#### Good result

    {
      "error": null,
      "ok": false,
      "result": {
        "token": "eXKexGfdM7zjnBa7rkzH",
        "username": "gitlab+deploy-token-51261"
      }
    }

#### Bad result

    {
      "error": "Login failed",
      "ok": false,
      "result": null
    }

