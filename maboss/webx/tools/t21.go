package main

/*
import (
	"github.com/hoisie/web"
	"time"
)

func hello(val string) string {
	const layout = "2006-01-02 15:04:05"
	return "hello " + val + time.Now().Format(layout)
}

func now(val string) string {
	const layout = "2006-01-02 15:04:05"
	return "hello " + val + time.Now().Format(layout)
}

func main() {

//	web.Get("/time", now)
	web.Get("/(.*)", hello)
	web.Run("0.0.0.0:9999")
}

*/

//package main

import (
	"C"
	"fmt"
	"time"
)

func main() {

	n, err := C.sqrt(-1)

	if err == nil {

		fmt.Println(n)
	}

	fmt.Println(time.Now().Unix())
	fmt.Println(time.Now().Format("2006/01/02 15:04:05 -0700 MST"))
	fmt.Println(time.Unix(1371646123, 0))
}
