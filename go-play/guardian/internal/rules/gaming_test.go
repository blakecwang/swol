package rules

import (
	"guardian/internal/model"
	"testing"
	"time"
)

func TestDetectGaming(t *testing.T) {
	e := model.Event{
		StudentID: 1,
		Timestamp: time.Now(),
		URL:       "https://roblocks.com",
		DOMText:   "Building castles in minecraft",
	}

	got := DetectGaming(e)

	want := []model.Alert{
		{
			StudentID: e.StudentID,
			RuleName:  "gaming",
			Match:     "minecraft",
		},
		{
			StudentID: e.StudentID,
			RuleName:  "gaming",
			Match:     "roblocks",
		},
	}

	if len(got) != len(want) {
		t.Fatalf("len(got)=%d, len(want)=%d\n", len(got), len(want))
	}

	for i, want_alert := range want {
		got_alert := got[i]

		if got_alert != want_alert {
			t.Fatalf("got_alert=%+v, want_alert=%+v\n", got_alert, want_alert)
		}
	}
}
