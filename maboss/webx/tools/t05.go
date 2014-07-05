package main

import (
	"fmt"
	"log"
)

func max(a int, b int) (c int, B int) {
	if a > b {
		c = a
		B = a
	}
	c = b
	B = b

	return
}

func add1(a *int) {
	*a = *a + 3
	//return *a
}

func main() {
	sum := 0
	for index := 0; index < 10; index++ {
		sum += index
	}

	x := 3

	var z *int = &x

	println(*z)
	println(&x)
	add1(&x)

	//fmt.Println("x+3 = ", x1) // 应该输出 "x+1 = 4"
	fmt.Println("x = ", x)

	log.Println("info")

	_ = 123

	for i := 0; i < 5; i++ {
		defer fmt.Printf("%d ", i)
	}

	m, _ := max(10, 22)

	fmt.Println(m)

	fmt.Println("sum is equal to ", sum)

}
