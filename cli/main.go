package main


import (
  "gopkg.in/yaml.v2"
  "os"
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
)


type Request struct {
	URL      string `json:"url"`
	Username string `json:"username"`
	Password string `json:"password"`
	Name     string `json:"name"`
	Server   string `json:"server"`
}

type Result struct {
    Token string
    Username string
    Dockerconfigjson string
}

type Answer struct {
  Error string
  Ok bool
  Result Result
}



func main() {
	endpoint := flag.String("endpoint", "https://gitlab-create-deploy-token.herokuapp.com/", "URL")
	debug := flag.Bool("debug", false, "debug")
	output := flag.String("output", "json", "Possible values [json,yaml,base64,k8s]")

	url := flag.String("url", "https://gitlab.com/group/project/", "url to project web page")
	username := flag.String("username", "", "GITLAB_USERNAME")
	password := flag.String("password", "", "GITLAB_PASSWORD")
	name := flag.String("name", "k8s", "name for deploy token")
	server := flag.String("server", "registry.gitlab.com", "docker registry domain")


	flag.Parse()

	
	if *username == "" {
    if *debug {
      fmt.Println("username not in command args, reading from env")
    }
    *username = os.Getenv("GITLAB_USERNAME")
	}

	if *password == "" {
    if *debug {
      fmt.Println("password not in command args, reading from env")
    }
    *password = os.Getenv("GITLAB_PASSWORD")
	}

	if *debug {
		fmt.Println("endpoint: ", *endpoint)
		fmt.Println("url: ", *url)
		fmt.Println("username: ", *username)
// 		fmt.Println("password: ", *password)
		fmt.Println("name: ", *name)
		fmt.Println("server: ", *server)
	}



	r := Request{
		URL:      *url,
		Username: *username,
		Password: *password,
		Name:     *name,
		Server:   *server,
	}

	b, err := json.Marshal(r)
	if err != nil {
		panic(err)
	}

	req, err := http.NewRequest("POST", *endpoint, bytes.NewBuffer(b))
	if err != nil {
		panic(err)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	defer resp.Body.Close()
	if err != nil {panic(err)}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {panic(err)}

  var answer Answer
  err = json.Unmarshal(body, &answer)
	if err != nil {panic(err)}

  if answer.Ok != true {
    panic(answer.Error)
  }



	switch *output {
  	case "json":
    	fmt.Println(string(body))

  	case "base64":
      fmt.Println(answer.Result.Dockerconfigjson)

  	case "yaml":
      y, err := yaml.Marshal(&answer)
      if err != nil { panic(err) }
    	fmt.Println(string(y))

  	case "k8s":
      fmt.Println(fmt.Sprintf("apiVersion: v1\nkind: Secret\nmetadata:\n  name: {{ .Release.Name }}-imagepullsecret\ndata:\n  .dockerconfigjson: %s\ntype: kubernetes.io/dockerconfigjson", answer.Result.Dockerconfigjson))

  	default:
    	fmt.Println(string(body))
	}


}
