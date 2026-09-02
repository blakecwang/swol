package rules

import (
	"guardian/internal/model"
	"strings"
)

func DetectGaming(e model.Event) []model.Alert {
	rule := "gaming"

	alerts := []model.Alert{}

	gamingTerms := []string{
		"minecraft",
	}

	for _, term := range gamingTerms {
		if strings.Contains(e.DOMText, term) {
			alerts = append(alerts, model.Alert{
				StudentID: e.StudentID,
				Rule:      rule,
			})
		}
	}

	return alerts
}
