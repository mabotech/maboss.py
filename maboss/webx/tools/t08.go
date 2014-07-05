package main

import (
	"errors"
	"fmt"
	"log"
	"strconv"
)

func p1() (int, error) {

	defer func() {
		//log.Println("defer:")
		if x := recover(); x != nil {
			fmt.Println("x:", x)
			//	return 2
		} else {
			fmt.Println("else")
			//return 1
		}

	}()

	i, err := strconv.Atoi("0x00")
	fmt.Println(i)

	//log.Println(err)
	//_ = err

	if err != nil {
		v := errors.New("raise error in p1()")
		
		log.Fatalln("fatal:",err)
		
		return -1, v
		panic(err)
		fmt.Println("after")
	}

	/*
		if err != nil {

			log.Println(i)
		} else {

			log.Println("error:",err)

		}
	*/
	return 011, nil

}

func main() {
	//   var buf [1<<31]byte
	//    buf[len(buf)-1] = 0

	v, e := p1()

	if e == nil {

		fmt.Println(v)

	} else {

		fmt.Println(e)

	}

	log.Println("ok")

}

/*

var ptr *byte

func main() {
        var buf [1<<31]byte
        buf[len(buf)-1] = 1
        ptr = &buf[0]

        println(1<<2)
        println(1024>>10)
        println(*ptr)
}
*/
