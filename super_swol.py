#!/usr/bin/env python
from __future__ import annotations

from datetime import datetime, timedelta
import random

import pandas as pd
from pandas import Series


GOOGLE_DOC_URL = "https://docs.google.com/spreadsheets/d/11lRtA-7zxK1OUACGokvvH60mWBB3i7--0D8jwCrCuKg/gviz/tq?tqx=out:csv&sheet=EXERCISES"
DAYS = ("PUSH", "PULL", "LEG", "PUSH", "PULL", "LEG")
EXERCISE_PAIRS_PER_DAY = 3


class Exercise:
    def __init__(self, name: str, muscles: list[str], weight: str, day: str, bench: str) -> None:
        self.name = name
        self.muscles = muscles
        self.weight = weight
        self.day = day
        self.bench = bench


class Workout:
    def __init__(self, exercises: list[Exercise]) -> None:
        self.exercises = exercises


class SuperSwol:
    def __init__(self) -> None:
        self.all_exercises: list[Exercise] = []
        self.workouts: list[Workout] = []

    def _construct_exercise(self, row: Series) -> Exercise:
        return Exercise(
            name=row["EXERCISE"],
            muscles=[muscle.strip().lower() for muscle in row["MUSCLES"].split(",")],
            weight=row["WEIGHT"],
            day=row["DAY"],
            bench=row["BENCH"],
        )

    def _get_all_exercises(self) -> list[Exercise]:
        df = pd.read_csv(GOOGLE_DOC_URL)
        exercises = [self._construct_exercise(row) for _, row in df.iterrows()]
        return exercises

    def _calculate_compatibility_score(self, exercise_a: Exercise, exercise_b: Exercise) -> float:
        common_muscles = set(exercise_a.muscles) & set(exercise_b.muscles)
        if count := len(common_muscles) > 0:
            weight = 1.0 / count
        else:
            weight = 1.1
        return weight

    def _find_compatible_exercise(self, exercise_a: Exercise, exercise_pool: list[Exercise]) -> Exercise:
        compatibility_scores = [self._calculate_compatibility_score(exercise_a, exercise_b) for exercise_b in exercise_pool]
        exercise_b = random.choices(exercise_pool, weights=compatibility_scores)[0]
        return exercise_b

    def _create_workout(self, day: str) -> Workout:
        exercise_pool = [ex for ex in self.all_exercises if ex.day == day]
        sample = random.sample(exercise_pool, EXERCISE_PAIRS_PER_DAY)
        sample_names = [ex.name for ex in sample]
        exercise_pool = [ex for ex in exercise_pool if ex.name not in sample_names]

        exercises = []
        for exercise_a in sample:
            exercise_b = self._find_compatible_exercise(exercise_a, exercise_pool)
            exercises.extend([exercise_a, exercise_b])
            exercise_pool = [ex for ex in exercise_pool if ex.name != exercise_b.name]
        return Workout(exercises)

    def _print_workout(self, workout: Workout, day: str) -> None:
        print(day)
        for exercise in workout.exercises:
            print(exercise.name)
        print()

    def get_swol(self) -> None:
        self.all_exercises = self._get_all_exercises()
        for day in DAYS:
            workout = self._create_workout(day)
            self._print_workout(workout, day)


if __name__ == "__main__":
    SuperSwol().get_swol()
