package main

import (
	"testing"
	"time"
)

func TestAverageDuration(t *testing.T) {
	durations := map[string]time.Duration{
		"a": 100 * time.Millisecond,
		"b": 200 * time.Millisecond,
		"c": 300 * time.Millisecond,
	}

	got := AverageDuration(durations)

	want := 200 * time.Millisecond

	if got != want {
		t.Errorf("got %v, want %v", got, want)
	}
}
