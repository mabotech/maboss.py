
package main

import (

"fmt"

)

func main() {

    const Pi float64 = 3.1415926
    
    var r float64 = 2
    
    var s string = `Pi * r *rPi * r *r`
    
    s1 := "hello"
    s1 = `s
    11
    
    ` + s1[1:]
    
    fmt.Println(s1)
    
    v := Pi * r *r
    
    fmt.Println(s, v)
    
    done := make(chan bool)

    values := []string{"a", "b", "c"}
    for _, v := range values {
        c := v // create a new 'v'.
        go func() {
            fmt.Println(c)
            done <- true
        }()
    }

    for _, v := range values {
        go func(u string) {
            fmt.Println(u)
            done <- true
        }(v)
    }

    // wait for all goroutines to complete before exiting
    for x := range values {
        fmt.Println("x:",x)
        <-done
    }
}