package main

import (
	"fmt"
	. "github.com/looplab/fsm"
	"strings"
)

func init() {

	fmt.Println("in Init...")
	fmt.Println(strings.Repeat("==", 20))

}

func main() {

	fsm := NewFSM(
		"red",
		Events{
			{Name: "warn", Src: []string{"green"}, Dst: "yellow"},
			{Name: "panic", Src: []string{"yellow"}, Dst: "red"},
			{Name: "panic", Src: []string{"green"}, Dst: "red"},
			{Name: "calm", Src: []string{"red"}, Dst: "yellow"},
			{Name: "clear", Src: []string{"yellow"}, Dst: "green"},
		},
		Callbacks{
			"before_warn": func(e *Event) {
				fmt.Println("before_warn")
			},
			"before_event": func(e *Event) {
				fmt.Println("before_event")
			},
			"leave_green": func(e *Event) {
				fmt.Println("leave_green")
			},
			"leave_state": func(e *Event) {
				fmt.Println("leave_state")
			},
			"enter_yellow": func(e *Event) {
				fmt.Println("enter_yellow")
			},
			"enter_green": func(e *Event) {
				fmt.Println("enter_green")
			},
			"enter_state": func(e *Event) {
				//	fmt.Println("enter_state")
			},
			"after_warn": func(e *Event) {
				fmt.Println("after_warn")
			},
			"after_event": func(e *Event) {
				fmt.Println("after_event")
			},
		},
	)

	fmt.Println(fsm.Current())

	b := fsm.Can("warn")

	fmt.Println(b)

	if b {

		err := fsm.Event("warn")

		if err != nil {
			fmt.Println(err)
		}
		fmt.Println(fsm.Current())
	} else {

	}
	err1 := fsm.Event("calm")
	if err1 != nil {
		fmt.Println(err1)
	}
	fmt.Println(fsm.Current())

}
