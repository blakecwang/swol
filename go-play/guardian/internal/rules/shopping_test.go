package rules

import (
	"guardian/internal/model"
	"testing"
)

func TestDetectShopping(t *testing.T) {
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
		{
			name: "url",
			event: model.Event{
				URL: "https://amazon.com",
			},
			wantAlerts: 1,
		},
		{
			name: "dom",
			event: model.Event{
				DOMText: "WHERE CAN I BUY SOME FLY SNEAKERS",
			},
			wantAlerts: 1,
		},
	}

	for _, testCase := range testCases {
		t.Run(testCase.name, func(t *testing.T) {
			got := len(DetectShopping(testCase.event))
			want := testCase.wantAlerts

			if got != want {
				t.Fatalf("got=%d, want=%d\n", got, want)
			}
		})
	}
}
