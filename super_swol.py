#!/usr/bin/env python
from __future__ import annotations

from datetime import datetime, timedelta
import random

import pandas as pd
from pandas import Series


GOOGLE_DOC_URL = "https://docs.google.com/spreadsheets/d/11lRtA-7zxK1OUACGokvvH60mWBB3i7--0D8jwCrCuKg/gviz/tq?tqx=out:csv&sheet=EXERCISES"
DAYS = ("PUSH", "PULL", "LEG", "PUSH", "PULL", "LEG")
EXERCISE_PAIRS_PER_DAY = 3

"""
TODO
- rate a workout higher if it has fewer weight changes
"""

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

    def _clean(self, val: Any) -> str:
        clean_val = str(val).strip()
        return clean_val

    def _construct_exercise(self, row: Series) -> Exercise:
        return Exercise(
            name=self._clean(row["EXERCISE"]),
            muscles=[muscle.strip() for muscle in self._clean(row["MUSCLES"]).split(",")],
            weight=self._clean(row["WEIGHT"]),
            day=self._clean(row["DAY"]),
            bench=self._clean(row["BENCH"]),
        )

    def _get_all_exercises(self) -> list[Exercise]:
        df = pd.read_csv(GOOGLE_DOC_URL)
        exercises = [self._construct_exercise(row) for _, row in df.iterrows()]
        return exercises

    def _is_compatible(self, exercise_a: Exercise, exercise_b: Exercise) -> bool:
        is_weight_compatible = (
            exercise_a.weight == exercise_b.weight or
            exercise_a.weight == "50" or
            exercise_b.weight == "50"
        )
        is_bench_compatible = (
            exercise_a.bench == exercise_b.bench or
            pd.isnull(exercise_a.bench) or
            pd.isnull(exercise_b.bench)
        )
        is_compatible = is_weight_compatible and is_bench_compatible
        return is_compatible

    def _calculate_muscle_coverage_score(self, exercise_a: Exercise, exercise_b: Exercise) -> float:
        common_muscles = set(exercise_a.muscles) & set(exercise_b.muscles)
        if count := len(common_muscles) > 0:
            weight = 1.0 / count
        else:
            weight = 2.0
        return weight

    def _find_compatible_exercise(self, exercise_a: Exercise, exercise_pool: list[Exercise]) -> Exercise:
        exercise_pool = [exercise_b for exercise_b in exercise_pool if self._is_compatible(exercise_a, exercise_b)]
        muscle_coverage_scores = [self._calculate_muscle_coverage_score(exercise_a, exercise_b) for exercise_b in exercise_pool]
        exercise_b = random.choices(exercise_pool, weights=muscle_coverage_scores)[0]
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
            print(exercise.name, exercise.weight, exercise.bench)
        print()

    def get_swol(self) -> None:
        self.all_exercises = self._get_all_exercises()
        for day in DAYS:
            workout = None
            counter = 0
            while workout is None and counter < 20:
                try:
                    workout = self._create_workout(day)
                except IndexError:
                    pass
                counter += 1
            self._print_workout(workout, day)


if __name__ == "__main__":
    SuperSwol().get_swol()
