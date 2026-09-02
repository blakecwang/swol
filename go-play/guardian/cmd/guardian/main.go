package main

import (
	"fmt"
	"guardian/internal/model"
	"guardian/internal/rules"
	"time"
)

func main() {
	event := model.Event{
		StudentID: 1,
		Timestamp: time.Now(),
		DOMText:   "Building castles in minecraft",
	}

	alerts := rules.DetectGaming(event)

	fmt.Printf("event: %+v\n", event)

	for _, alert := range alerts {
		fmt.Printf("alert: %+v\n", alert)
	}
}
