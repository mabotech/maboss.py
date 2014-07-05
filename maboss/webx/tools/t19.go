package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"strings"
)

func main() {

	s := []string{"foo", "bar", "baz"}
	
	fmt.Println("a:"+strings.Join(s, ", "))

	file, err := os.Open("a1.csv")

	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	defer file.Close()

	reader := csv.NewReader(file)

	for {

		record, err := reader.Read()

		if err == io.EOF {
			break
		} else if err != nil {
			fmt.Println("Error:", err)
			return
		}
		var l int = len(record)
		if l == 3 {
			fmt.Printf("insert into values( %v,%v,%v)\n", record[0], record[1], record[2])
		} else {
			fmt.Println(record) // record has the type []string
		}
	}
}
