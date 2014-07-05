package main

import (
	"fmt"
	"os"
)

func main() {

	fh, err := os.Open("a1.txt")

	if err != nil {
		v := os.Read(fh)
		fmt.Println(v)
	}
	
	defer os.Close()

}
