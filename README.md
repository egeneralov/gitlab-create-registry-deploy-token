# Gitlab: create registry deploy token

Create gitlab registry read-only token for project. Also you can auto-generate tokens for k8s deployments on-the-fly.

Tested with gitlab.com and omnibus installation.

## How to

#### Create json file

##### minimal

    {
      "url": "https://gitlab.com/group/project/",
      "username": "user@domain.tld",
      "password": "password",
      "name": "name-of-deploy-token",
    }

##### extended

    {
      "url": "https://gitlab.com/group/project/",
      "username": "user@domain.tld",
      "password": "password",
      "name": "k8s",
      "server": "registry.gitlab.com"
    }

#### Load into script

    curl -s -d@some.json https://gitlab-create-deploy-token.herokuapp.com/ | jq

#### Good result

##### minimal

    {
      "error": null,
      "ok": true,
      "result": {
        "token": "FuuLyGGygF2cXQ2DxqRQ",
        "username": "gitlab+deploy-token-6"
      }
    }

##### extended

    {
      "error": null,
      "ok": true,
      "result": {
        "dockerconfigjson": "eyJhdXRocyI6IHsicmVnaXN0cnkuZ2l0bGFiLnNoYXJlZCI6IHsidXNlcm5hbWUiOiAiZ2l0bGFiK2RlcGxveS10b2tlbi01IiwgInBhc3N3b3JkIjogIlVla0hnbXN6V3pBTl9fa3AyMmdCIiwgImF1dGgiOiAiWjJsMGJHRmlLMlJsY0d4dmVTMTBiMnRsYmkwMU9sVmxhMGhuYlhONlYzcEJUbDlmYTNBeU1tZEMifX19",
        "token": "UekHgmszWzAN__kp22gB",
        "username": "gitlab+deploy-token-5"
      }
    }

#### Bad result

    {
      "error": "Login failed",
      "ok": false,
      "result": null
    }

### Source code

[https://github.com/egeneralov/gitlab-create-registry-deploy-token](https://github.com/egeneralov/gitlab-create-registry-deploy-token)


##### example usage for extended mode


    cat << EOF > secret.yaml
    apiVersion: v1
    data:
      .dockerconfigjson: $(curl -sd'{"url":"https://gitlab.com/group/project/","username":"user@domain.tld","password":"password","name":"k8s","server": "registry.gitlab.com"}' http://127.0.0.1:8080/ | jq -r .result.dockerconfigjson)
    kind: Secret
    metadata:
      name: {{ .Release.Name }}-imagepullsecret
    type: kubernetes.io/dockerconfigjson
    EOF

##### todo:

  - add "expire" support
  - add "read_repository" support
  - add table with supported gitalb versions

