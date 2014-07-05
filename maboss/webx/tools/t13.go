package main

import "time"
import "fmt"

func main() {

	// Tickers use a similar mechanism to timers: a
	// channel that is sent values. Here we'll use the
	// `range` builtin on the channel to iterate over
	// the values as they arrive every
	ticker := time.NewTicker(time.Millisecond * 500)
	go func() {

		//fmt.Println(<-ticker.C)
		for t := range ticker.C {
			fmt.Println("Tick at:", t)
		}
	}()
	// Tickers can be stopped like timers. Once a ticker
	// is stopped it won't receive any more values on its
	// channel. We'll stop ours after 1500ms.

	for {
		time.Sleep(time.Millisecond * 2500)
	}
}
