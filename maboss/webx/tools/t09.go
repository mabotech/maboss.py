package main
 
import(
    "fmt"
    //"os"
)
 
var user = ""
func inita() {
    defer func(){
        fmt.Print("defer##\n")
    }()
    if user == "" {
        fmt.Print("@@@before panic\n")
        panic("no value for user\n")
        fmt.Print("!!after panic\n")
    }
}
 
func throwsPanic (f func()) (b bool){
    defer func(){
        if x:= recover(); x != nil{
            fmt.Print(x)
            b = true
        }
    }()
    f()
    fmt.Print("after the func run")
    return
}
 
func main(){
    throwsPanic(inita)
}