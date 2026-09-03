package rules

import (
	"guardian/internal/model"
	"strings"
)

func DetectGaming(e model.Event) []model.Alert {
	ruleName := "gaming"

	gamingTerms := []string{
		"minecraft",
		"roblocks",
	}

	alerts := []model.Alert{}

	inputs := []string{
		e.URL,
		e.DOMText,
	}

	for _, term := range gamingTerms {
		for _, input := range inputs {
			inputLower := strings.ToLower(input)
			if strings.Contains(inputLower, term) {
				alert := model.Alert{
					StudentID: e.StudentID,
					RuleName:  ruleName,
					Match:     term,
				}
				alerts = append(alerts, alert)
			}
		}
	}

	return alerts
}
