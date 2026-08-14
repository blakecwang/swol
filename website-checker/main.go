package main

import (
	"fmt"
	"net/http"
	"sync"
	"time"
)

func CheckWebsite(url string, wg *sync.WaitGroup) {
	defer wg.Done()

	startTime := time.Now()
	resp, err := http.Get(url)
	if err != nil {
		fmt.Printf("[%s] Failed to fetch: %v\n", url, err)
		return
	}
	defer resp.Body.Close()

	duration := time.Since(startTime)
	fmt.Printf("[%s] Status: %d (%v)\n", url, resp.StatusCode, duration)
}

func main() {
	websites := []string{
		"https://google.com",
		"https://github.com",
		"https://go.dev",
		"https://reddit.com",
		"https://stackoverflow.com",
	}

	var wg sync.WaitGroup

	fmt.Println("Starting concurrent website checks...")
	totalStart := time.Now()

	for _, url := range websites {
		wg.Add(1)
		go CheckWebsite(url, &wg)
	}

	wg.Wait()

	totalDuration := time.Since(totalStart)
	fmt.Printf("\nAll checks completed in %v.\n", totalDuration)
}
