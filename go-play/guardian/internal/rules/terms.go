package rules

import (
	"guardian/internal/model"
	"strings"
)

func DetectTerms(event model.Event, ruleName string, terms []string) []model.Alert {
	alerts := []model.Alert{}

	inputs := []string{
		event.URL,
		event.DOMText,
	}

	for _, term := range terms {
		for _, input := range inputs {
			inputLower := strings.ToLower(input)
			if strings.Contains(inputLower, term) {
				alert := model.Alert{
					StudentID: event.StudentID,
					RuleName:  ruleName,
					Match:     term,
				}
				alerts = append(alerts, alert)
			}
		}
	}

	return alerts
}

func DetectGaming(event model.Event) []model.Alert {
	ruleName := "gaming"

	gamingTerms := []string{
		"minecraft",
		"roblocks",
	}

	return DetectTerms(event, ruleName, gamingTerms)
}

func DetectShopping(event model.Event) []model.Alert {
	ruleName := "shopping"

	shoppingTerms := []string{
		"amazon",
		"sneakers",
	}

	return DetectTerms(event, ruleName, shoppingTerms)
}

func DetectProfanity(event model.Event) []model.Alert {
	ruleName := "profanity"

	profanityTerms := []string{
		"fuck",
		"shit",
	}

	return DetectTerms(event, ruleName, profanityTerms)
}
