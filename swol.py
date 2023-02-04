#!/usr/bin/env python

from datetime import datetime, timedelta
import random

import pandas as pd


"""
TODO
- add data validation
- create workouts a week at a time so exercises don't repeat the next day
- incorporate weights so that exercise pairs are convenient
- rank exercise pairs higher if there are more different
"""


FOR_TOMORROW = False
SCHEDULE = (
    ("arms", "shoulders"),  # Monday
    ("chest", "back"),      # Tuesday
    ("arms", "shoulders"),  # Wednesday
    ("core", "legs"),       # Thursday
    ("chest", "back"),      # Friday
    ("arms", "shoulders"),  # Saturday
    ("chest", "back"),      # Sunday
)
EXERCISES_PER_GROUP = 3
MUSCLE_GROUPS = {
    "core": [
        "core",
        "obliques",
    ],
    "legs": [
        "abductors",
        "adductors",
        "ankles",
        "calves",
        "glutes",
        "hamstrings",
        "quads",
    ],
    "arms": [
        "arms",
        "biceps",
        "brachialis",
        "brachioradialis",
        "forearms",
        "grip strength",
        "triceps",
    ],
    "shoulders": [
        "shoulders",
        "deltoids",
        "rotator cuffs",
        "traps",
    ],
    "chest": [
        "pecs",
        "serratus anterior",
        "upper chest"
    ],
    "back": [
        "back",
        "erectors",
        "lats",
        "lower back",
        "upper back",
        "rhomboids",
    ],
}
OPTIMIZATION_ATTEMPTS = 10
NUM_WORKOUTS = 7


def swol():
    # fetch and organize data into convenient data structures
    muscles_by_exercise = get_muscles_by_exercise()
    exercises_by_muscle = get_exercises_by_muscle(muscles_by_exercise)
    breakpoint()
    exercises_by_group = get_exercises_by_group(exercises_by_muscle)

    # create and print workouts
    timestamp = datetime.now()
    todays_workout = []
    for _ in range(7):
        timestamp += timedelta(days=1)
        todays_workout, groups = get_todays_workout(
            muscles_by_exercise,
            exercises_by_group,
            timestamp,
            todays_workout,
        )
        print_todays_workout(todays_workout, groups, timestamp)


def get_todays_workout(
    muscles_by_exercise,
    exercises_by_group,
    timestamp,
    yesterdays_workout,
):
    groups = get_muscle_groups(timestamp)
    possible_workouts = [get_workout(exercises_by_group, groups, yesterdays_workout) for _ in range(OPTIMIZATION_ATTEMPTS)]
    todays_workout = choose_workout(possible_workouts, muscles_by_exercise)

    return todays_workout, groups


def print_todays_workout(todays_workout, groups, timestamp):
    DATE_FORMAT = "%A, %-m/%-d/%Y"

    print(f"workout for {timestamp.strftime(DATE_FORMAT)} ({groups[0]}, {groups[1]})".upper())
    for exercise in todays_workout:
        print(exercise)
    print("\n\n")


def get_workout(exercises_by_group, groups, yesterdays_workout):
    def sort_exercises(workout):
        # TODO implement
        return workout

    workout = []
    for group in groups:
        possible_exercises = set(exercises_by_group[group])  # dedupe exercises in a group
        possible_exercises = possible_exercises.difference(set(workout))  # dedupe exercises between groups
        possible_exercises = possible_exercises.difference(set(yesterdays_workout))  # dedupe exercises from yesterday
        sample = random.sample(possible_exercises, EXERCISES_PER_GROUP)
        workout.extend(sample)

    try:
        workout = sort_exercises(workout)
    except AssertionError:
        print("FAILED TO SORT EXERCISES!!")
        return get_workout(exercises_by_group, groups, yesterdays_workout)

    return workout


def choose_workout(possible_workouts, muscles_by_exercise):
    def get_score(muscles):
        """
        choose workouts that focus on similar muscles
        """
        score = 0
        muscles_set = set(muscles)
        for muscle in muscles_set:
            score += 2 ** muscles.count(muscle)

        return score

    todays_workout = None
    score = -1
    for workout in possible_workouts:
        muscles = [muscle for exercise in workout for muscle in muscles_by_exercise[exercise]]
        curr_score = get_score(muscles)
        if curr_score > score:
            todays_workout = workout
            score = curr_score

    return todays_workout


def get_muscles_by_exercise():
    SHEET_ID = "11lRtA-7zxK1OUACGokvvH60mWBB3i7--0D8jwCrCuKg"
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv")

    muscles_by_exercise = {}
    for _, row in df.iterrows():
        exercise = row["EXERCISE"]
        muscles = [m.strip() for m in row["MUSCLES"].split(",")]
        muscles_by_exercise[exercise] = muscles

    return muscles_by_exercise


def get_exercises_by_muscle(muscles_by_exercise):
    exercises_by_muscle = {}
    for exercise, muscles in muscles_by_exercise.items():
        for muscle in muscles:
            exercises_by_muscle[muscle] = exercises_by_muscle.get(muscle, [])
            exercises_by_muscle[muscle].append(exercise)

    return exercises_by_muscle


def get_exercises_by_group(exercises_by_muscle):
    exercises_by_group = {}
    for group, muscles in MUSCLE_GROUPS.items():
        exercises_by_group[group] = exercises_by_group.get(group, [])
        for muscle in muscles:
            exercises = exercises_by_muscle.get(muscle, [])
            exercises_by_group[group].extend(exercises)

    return exercises_by_group


def get_muscle_groups(timestamp):
    return SCHEDULE[timestamp.weekday()]


swol()
