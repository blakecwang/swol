package model

import "time"

type Event struct {
	StudentID int
	Timestamp time.Time
	URL       string
	DOMText   string
}
