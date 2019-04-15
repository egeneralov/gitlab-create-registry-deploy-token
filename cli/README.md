# gitlab-create-registry-deploy-token

Command line utility - client for [gitlab-create-registry-deploy-token](https://github.com/egeneralov/gitlab-create-registry-deploy-token.git) api.

## build

    cd cli/
    export CGO_ENABLED=0 GOOS=darwin GOARCH=amd64
    go build -a -tags netgo -ldflags '-w' -v -o ${GOPATH:-~/go}/bin/gitlab-create-registry-deploy-token main.go

#### -help

    Usage of gitlab-create-registry-deploy-token:
      -debug
        	debug
      -endpoint string
        	URL (default "https://gitlab-create-deploy-token.herokuapp.com/")
      -name string
        	name for deploy token (default "k8s")
      -output string
        	Possible values [json,yaml,base64,k8s] (default "json")
      -password string
        	GITLAB_PASSWORD
      -server string
        	docker registry domain (default "registry.gitlab.com")
      -url string
        	url to project web page (default "https://gitlab.com/group/project/")
      -username string
        	GITLAB_USERNAME

#### -url

Full web url to main page for your gitlab project. Must ends with `/`.

#### -debug

Provide additional information. Note: password will be hidden.

    username not in command args, reading from env
    password not in command args, reading from env
    endpoint:  https://gitlab-create-deploy-token.herokuapp.com/
    url:  https://gitlab.com/group/project/
    username:  user@domain.tld
    name:  k8s
    server:  registry.gitlab.com


#### -endpoint

URL to running [gitlab-create-registry-deploy-token](https://github.com/egeneralov/gitlab-create-registry-deploy-token.git) api.


#### auth

Username and password to login to gitlab ui. API method for deploy tokens not implimented, so i forced to emulate browser.

- `-username` if flag not provided will be sourced `GITLAB_USERNAME` environment variable
- `-password` if flag not provided will be sourced `GITLAB_PASSWORD` environment variable

#### -server

Docker registry to place to docker config.json field. Must be provided for correct result. Default `registry.gitlab.com`.

#### -output


##### json

Raw answer from api in json format

    {
      "error": null, 
      "ok": true, 
      "result": {
        "dockerconfigjson": "eyJhdXRocyI6IHsicmVnaXN0cnkuZ2l0bGFiLmNvbSI6IHsidXNlcm5hbWUiOiAiZ2l0bGFiK2RlcGxveS10b2tlbi02MDQzMiIsICJwYXNzd29yZCI6ICI1eVN0ODR6cHpKTTJwc21jcTRieCJ9fX0=", 
        "token": "5ySt84zpzJM2psmcq4bx", 
        "username": "gitlab+deploy-token-60432"
      }
    }


##### yaml

Raw answer from api in yaml format

    error: ""
    ok: true
    result:
      token: yLnf24e9Y5y9c_7ciiQR
      username: gitlab+deploy-token-60433
      dockerconfigjson: eyJhdXRocyI6IHsicmVnaXN0cnkuZ2l0bGFiLmNvbSI6IHsidXNlcm5hbWUiOiAiZ2l0bGFiK2RlcGxveS10b2tlbi02MDQzMyIsICJwYXNzd29yZCI6ICJ5TG5mMjRlOVk1eTljXzdjaWlRUiJ9fX0=


##### base64

Just .result.dockerconfigjson value.

    eyJhdXRocyI6IHsicmVnaXN0cnkuZ2l0bGFiLmNvbSI6IHsidXNlcm5hbWUiOiAiZ2l0bGFiK2RlcGxveS10b2tlbi02MDQzNCIsICJwYXNzd29yZCI6ICJ0YXY4VU1FVU01Z2lhb2lleXExeiJ9fX0=


##### k8s

Just ready helm template.

    apiVersion: v1
    kind: Secret
    metadata:
      name: {{ .Release.Name }}-imagepullsecret
    data:
      .dockerconfigjson: eyJhdXRocyI6IHsicmVnaXN0cnkuZ2l0bGFiLmNvbSI6IHsidXNlcm5hbWUiOiAiZ2l0bGFiK2RlcGxveS10b2tlbi02MDQzNSIsICJwYXNzd29yZCI6ICJKb0hvcW94ZGJyTV9MVGoyTTFSbSJ9fX0=
    type: kubernetes.io/dockerconfigjson
