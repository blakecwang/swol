package rules

import (
	"guardian/internal/model"
	"testing"
)

func TestDetectProfanity(t *testing.T) {
	testCases := []struct {
		name       string
		event      model.Event
		wantAlerts int
	}{
		{
			name: "safe",
			event: model.Event{
				URL: "https://wikipedia.com",
			},
			wantAlerts: 0,
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.name, func(t *testing.T) {
			got := len(DetectProfanity(testCase.event))
			want := testCase.wantAlerts

			if got != want {
				t.Fatalf("got=%d, want=%d\n", got, want)
			}
		})
	}
}
