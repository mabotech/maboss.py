package main

import (
	"os"
)

var user = os.Getenv("USER")

func init2() {

	println("init2")

}

func init() {

	init2()
	
	if user == "" {
		panic("no value for $USER")
	}



}

func main() {

}
