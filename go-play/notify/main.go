// A notifier program
package main

import "fmt"

type EmailNotifier struct {
	SentCount int
}

// send message via email
func (e *EmailNotifier) Send(message string) error {
	fmt.Printf("EMAIL: %s\n", message)
	e.SentCount++
	return nil
}

type SlackNotifier struct {
	SentCount int
}

// send message via slack
func (s *SlackNotifier) Send(message string) error {
	fmt.Printf("SLACK: %s\n", message)
	s.SentCount++
	return nil
}

type Notifier interface {
	Send(message string) error
}

// send message via all provided channels
func Broadcast(notifiers []Notifier, message string) error {
	for _, notifier := range notifiers {
		err := notifier.Send(message)
		if err != nil {
			return err
		}
	}
	return nil
}

func main() {
	email := &EmailNotifier{}

	var n Notifier = email
	fmt.Printf("n=%v\n", n)

	slack := &SlackNotifier{}

	err := Broadcast(
		[]Notifier{email, slack},
		"broadcast content",
	)

	fmt.Printf("err=%v\n", err)
	fmt.Printf("Emails sent: %d\n", email.SentCount)
	fmt.Printf("Slack messages sent: %d\n", slack.SentCount)
}
