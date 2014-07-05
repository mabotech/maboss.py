package main

import (
	"crypto/md5"
	"fmt"
	"io"
	"reflect"
	"math"
	//"encoding/csv"
)

func main() {
	// var buf [1<<31]byte
	var buf = new([1 << 2]byte)
	//println(*buf)

	h := md5.New()

	fmt.Println(reflect.TypeOf(h))

	io.WriteString(h, "mjj@mabotech.com")

	fmt.Printf("%x\n", h.Sum(nil))

	fmt.Println(h.Sum(nil))
	
	fmt.Println(math.Sin(math.Pi+1))

	fmt.Println(reflect.TypeOf(buf))

	buf[len(buf)-1] = 1
	fmt.Println(reflect.ValueOf(buf))
	fmt.Println(*buf)
	

	
}
