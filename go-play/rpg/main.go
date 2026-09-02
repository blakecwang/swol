package main

import "fmt"

type Character struct {
	Name   string
	Health int
}

type Monster struct {
	Species string
	Health  int
}

func (m *Monster) TakeDamage(amount int) {
	m.Health -= amount
}

func (m *Monster) Heal(amount int) {
	m.Health += amount
}

func (c *Character) TakeDamage(amount int) {
	c.Health -= amount
}

func (c *Character) Heal(amount int) {
	c.Health += amount
}

type Damageable interface {
	TakeDamage(amount int)
}

type Healable interface {
	Heal(amount int)
}

func Hit(target Damageable) {
	target.TakeDamage(10)
}

func Boost(target Healable) {
	target.Heal(20)
}

func main() {
	hero := Character{
		Name:   "Arthur",
		Health: 100,
	}

	goblin := Monster{
		Species: "goblin",
		Health:  100,
	}

	hero.TakeDamage(25)

	Hit(&hero)
	Hit(&goblin)

	Boost(&hero)
	Boost(&goblin)

	fmt.Printf("hero health: %d, goblin health: %d\n", hero.Health, goblin.Health)
}
