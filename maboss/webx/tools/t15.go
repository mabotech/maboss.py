package main

import (
"fmt"

"time"
)

func fibonacci(c, quit chan int) {
	x, y := 1, 1
	for {
		select {
		case c <- x:
			x, y = y, x+y
		case <-quit:
			fmt.Println("quit")
			return
		}
	}
}

func main() {
	c := make(chan int)
	quit := make(chan int)
	
	go fibonacci(c, quit)
	
	
	go func() {
		for i := 0; i < 10; i++ {
			fmt.Println("c:", <-c)
		}
		quit <- 0
	}()
	
	
	time.Sleep(time.Second * 3)
}
