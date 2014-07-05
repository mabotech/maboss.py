package main

import "fmt"

func fact(n int) (A int) {
	if n == 0 {
		return 1
	}
	A = n * fact(n-1)
	return
}

func main() {
	fmt.Println(fact(7))
}
