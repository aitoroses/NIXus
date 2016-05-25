package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
)

type Frontend struct {
	Name string `json:"name"`
	Port string `json:"port"`
}
type Backend struct {
	Addr     string `json:"addr"`
	Name     string `json:"name"`
	Rewrite  bool   `json:"rewrite"`
	Proccess string
}

type ContainerCfg struct {
	Config struct {
		Cmd []string
	}
}

func (m Backend) GetProccess() string {
	response, err := http.Get(fmt.Sprintf("http://%s/dockerapi/containers/%s/json", os.Getenv("HOST_IP"), m.Name))
	defer response.Body.Close()
	if err != nil {
		fmt.Printf("%s", err)
		os.Exit(1)
	}

	contents, err := ioutil.ReadAll(response.Body)
	if err != nil {
		fmt.Printf("%s", err)
		os.Exit(1)
	}

	data := []byte(contents)
	cfg := &ContainerCfg{}
	json.Unmarshal(data, cfg)

	return strings.Join(cfg.Config.Cmd, " ")
}

type Service struct {
	Backends  map[string][]Backend `json:"backends"`
	Frontends []Frontend           `json:"frontends"`
}
type Proxy map[string]Service

func parserJSON(v []byte) Proxy {
	res := Proxy{}
	json.Unmarshal(v, &res)
	return res
}

func getInfo() Proxy {
	response, err := http.Get(fmt.Sprintf("http://%s/proxy_info", os.Getenv("HOST_IP")))
	defer response.Body.Close()
	if err != nil {
		fmt.Printf("%s", err)
		os.Exit(1)
	}

	contents, err := ioutil.ReadAll(response.Body)
	if err != nil {
		fmt.Printf("%s", err)
		os.Exit(1)
	}
	data := []byte(contents)

	return parserJSON(data)
}

var tmp = template.Must(template.ParseFiles("./templates/index.html"))

func renderTemplate(w http.ResponseWriter, tmpl string, p interface{}) {
	err := tmp.ExecuteTemplate(w, tmpl+".html", p)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	p := getInfo()
	fmt.Println(r.URL)
	renderTemplate(w, "index", p)
}

func main() {
	mux := http.NewServeMux()
	//mux.Handle("/public/", http.StripPrefix("/public/", http.FileServer(http.Dir("./public"))))
	mux.Handle("/", http.HandlerFunc(indexHandler))

	fmt.Printf("Listening on port 3000 \n")
	err := http.ListenAndServe(":3000", mux)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}

}
