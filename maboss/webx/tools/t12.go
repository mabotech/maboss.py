package main

	

import "time"
import "fmt"
import "log"
	

func main() {

    log.Println("1")
    timer1 := time.NewTimer(time.Second * 2)

 

    a := <-timer1.C
    log.Println("2", a)
    fmt.Println("Timer 1 expired")
 

    timer2 := time.NewTimer(time.Second)
    go func() {
        <-timer2.C
        log.Println("3")
        fmt.Println("Timer 2 expired")
    }()
    
    //time.Sleep(2000)
    
    time.Sleep(time.Millisecond * 1500)
    
    stop2 := timer2.Stop()
    if stop2 {
    log.Println("4")
        fmt.Println("Timer 2 stopped")
    }
}
