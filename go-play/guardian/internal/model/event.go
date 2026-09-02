package model

import "time"

type Event struct {
	StudentID int
	Timestamp time.Time
	DOMText   string
}
