package main

import (
	"fmt"
	"net/http"
	"time"
)

type Result struct {
	URL        string
	StatusCode int
	Duration   time.Duration
	Error      error
}

func CheckWebsite(url string, results chan<- Result) {
	startTime := time.Now()
	resp, err := http.Get(url)
	if err != nil {
		results <- Result{
			URL:   url,
			Error: err,
		}
		return
	}
	defer resp.Body.Close()

	results <- Result{
		URL:        url,
		StatusCode: resp.StatusCode,
		Duration:   time.Since(startTime),
	}
}

func main() {
	results := make(chan Result)

	websites := []string{
		"https://google.com",
		"https://github.com",
		"https://go.dev",
		"https://reddit.com",
		"https://stackoverflow.com",
	}

	durations := map[string]time.Duration{}

	fmt.Println("Starting concurrent website checks...")
	totalStart := time.Now()

	for _, url := range websites {
		go CheckWebsite(url, results)
	}

	for range websites {
		result := <-results
		fmt.Printf("%s %d %v %v\n",
			result.URL,
			result.StatusCode,
			result.Duration,
			result.Error,
		)
		durations[result.URL] = result.Duration
	}

	totalDuration := time.Since(totalStart)

	fmt.Printf("\nAll checks completed in %v.\n", totalDuration)

	for website, duration := range durations {
		fmt.Printf("%s: %v\n", website, duration)
	}
}
