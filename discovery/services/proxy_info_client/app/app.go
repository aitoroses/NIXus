package main

import (
    "log"
    "net/http"
    "html/template"
)

var tmp = template.Must(template.ParseFiles("src/index.html"))

func renderTemplate(w http.ResponseWriter, tmpl string) {
    err := tmp.ExecuteTemplate(w, tmpl+".html", p)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
    }
}

func parserJSON(v interface {}) template.JS {
  a, _ := json.Marshal(v)
  return template.JS(a)
}

func getInfo() {
    response, _, err := http.Get("http://nixus.dev/proxy_info")
    if err != nil {
        fmt.Printf("%s", err)
        os.Exit(1)
    } else {
        defer response.Body.Close()
        contents, err := ioutil.ReadAll(response.Body)
        if err != nil {
            fmt.Printf("%s", err)
            os.Exit(1)
        }
        fmt.Printf("%s\n", string(contents))

        data := []byte(contents)

        return parserJSON(data)
    }
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
    //p, _ := getInfo()
    renderTemplate(w, "src/index")
}

func main() {
    http.HandleFunc("/", indexHandler) // set router
    err := http.ListenAndServe(":3000", nil) // set listen port
    if err != nil {
        log.Fatal("ListenAndServe: ", err)
    }
}
