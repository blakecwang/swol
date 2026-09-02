package main

import (
	"testing"
)

func TestHit(t *testing.T) {
	hero := Character{
		Name:   "Test",
		Health: 100,
	}

	Hit(&hero)

	got := hero.Health

	want := 90

	if got != want {
		t.Errorf("got %d, want %d", got, want)
	}
}
