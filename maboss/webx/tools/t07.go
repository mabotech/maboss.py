package main

import (
	"fmt"
	"log"
	"runtime"
	"time"
)

func say(s string) {

	//fmt.Println("v:",runtime.NumCPU)

	///fmt.Println(runtime.NumGoroutine)

	const longForm = "Jan 2, 2006 at 3:04pm (MST)"

	const shortForm = "2006-Jan-02"

	t, _ := time.Parse(longForm, "Feb 3, 2013 at 7:54pm (PST)")

	//~ fmt.Println("t:",t)
	log.Println("info here")
	//~ fmt.Println(`info:`, time.Now())

	t, _ = time.Parse(shortForm, "2013-Feb-03")

	_ = t
	//fmt.Println(t)

	for i := 0; i < 5; i++ {

		runtime.Gosched()

		fmt.Println(s)
		//log.Println(s)
	}
}

func main() {

	log.SetFlags(17)
	log.SetPrefix("log:--,")

	runtime.GOMAXPROCS(4)
	go say("world") //开一个新的Goroutines执行
	say("--hello")  //当前Goroutines执行
	//time.Sleep(100000)
	//for {
	//time.Sleep(1000)
	//	fmt.Println(".")
	//}
}
