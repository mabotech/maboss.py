package main

import (
	//"fmt"
	"log"
	"time"
)

func main() {

	c := make(chan int64, 5)

	defer close(c)
	c <- 10

	timeout := make(chan bool)

	defer close(timeout)

	go func() {
		time.Sleep(time.Second)
		timeout <- true
	}()

	go func() {
		log.Println("1")
		select {

		case <-timeout:
			log.Println("timeout...")

		case <-c:
			log.Println("Read a date.")

		}
	}()

	time.Sleep(time.Second * 2)
	log.Println("done")
}
