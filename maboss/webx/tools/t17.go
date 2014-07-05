package main

import (
	"fmt"
	"log"
	"time"
)

func main() {
	tick := time.Tick(1e8)

	boom := time.After(5e8)

	log.Println(5e7)
	
	LOOP:
	
	for {

		select {
		case <-tick:
			log.Println("tick.")
		case <-boom:
			fmt.Println("BOOM!")
			//tick.Stop()
			
			break LOOP
			return
		default:
			fmt.Println("    .")
			time.Sleep(5e7)
		}
	}
	
		

	log.Println("2")
	


}
