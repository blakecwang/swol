package main

import "fmt"

func main() {
	messages := make(chan string)

	go func() {
		messages <- "hello"
	}()

	msg := <-messages

	fmt.Println(msg)
}
