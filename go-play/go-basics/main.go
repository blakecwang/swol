package main

import "fmt"

func main() {
	mySlice := []int{1, 2, 3}
	fmt.Printf("%v\n", mySlice)

	myMap := map[string]string{
		"key1": "val1",
		"key2": "val2",
	}
	fmt.Printf("%v\n", myMap)

	// 3 parts: init, end condition, post action
	for i := 0; i < 5; i++ {
		fmt.Printf("%d\n", i)
	}

	// conditional - goes until condition is not true (like 'while')
	i := 0
	for i < 5 {
		fmt.Printf("%d\n", i)
		i++
	}

	// infinite - `break`/`return` to exit loop
	j := 0
	for {
		fmt.Printf("%d\n", j)
		if j == 5 {
			break
		} else {
			j++
		}
	}

	// for range
	for index, number := range mySlice {
		fmt.Printf("index=%d, number=%d\n", index, number)
	}

	// for range one value - gives you index
	for v := range mySlice {
		fmt.Printf("%v\n", v)
	}

	// iterate over maps
	for k, v := range myMap {
		// fmt.Printf("%s: %s\n", k, v)
	}
}

// is map key order guaranteed?
// what's the difference between slice and array?
