


package main

import (

    "fmt"
    "os"
)

func main(){
  
    i := 2
    
    switch  {
    
        case i > 1 : fmt.Println(">")
        case i == 1 : fmt.Println("=")
        case i < 1 : fmt.Println("<")
    
    }
    
    f, err := os.Open("t03.py")
    if err != nil{
    
        fmt.Println("hi, read failed")
    
    }
    
    buf := make([]byte, 10)
    
    f.Read(buf[0:])
    
    for _, c := range buf{
        fmt.Println( chr(c) )
    }
    
    defer f.Close()
    
    var c string = "c"
    
    switch c {
    
        case  " ": fmt.Println("hi")
        default : fmt.Println("default")
    }
    
    if i > 5{
    
        fmt.Println("gt")
    
    }else{
        fmt.Println("not gt")
        
    }
    
    fmt.Printf("hi:%v\n", i)
    
    var j int = 9
    var x string = "abc"
    
    x = x+"012"
    
    fmt.Println(x)
    
    for i=0;i<j;i++{
    
        fmt.Printf("%v,", i)
    
    }
    
    var v  []int = make([]int, 20)
    
    fmt.Println(v)
    
    
    array := [...]float64{7.2, 8.5, 9.1, 12.5, 54.9}
    fmt.Print("\n")
    fmt.Println("len:")
    fmt.Println(len(array))
    
    fmt.Println(array[0])
    
    fmt.Print("\n")
    
}