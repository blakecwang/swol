#!/usr/bin/env python

import random

import pandas as pd


"""
TODO
- add data validation
"""


NUM_WORKOUTS = 4
EXERCISES_PER_GROUP = 3
FOCUS_MUSCLE_GROUPS = ("arms", "shoulders")
OPTIMIZATION_ATTEMPTS = 10
SHEET_ID = "11lRtA-7zxK1OUACGokvvH60mWBB3i7--0D8jwCrCuKg"
EXERCISES_SHEET_NAME = "EXERCISES"
MUSCLE_GROUPS_SHEET_NAME = "MUSCLE_GROUPS"
DATE_FORMAT = "%A, %-m/%-d/%Y"
MUSCLE_FACTOR = 2  # higher number will select workouts that focus on certain muscles
WEIGHT_FACTOR = 2  # higher number will select workouts that focus on certain weights
PAIR_FACTOR = 3  # higher number will select workouts with pairs that overlap less


def arms():
    # fetch and organize data into convenient data structures
    muscles_by_exercise = get_muscles_by_exercise()
    exercises_by_muscle = get_exercises_by_muscle(muscles_by_exercise)
    muscle_groups = get_muscle_groups()
    exercises_by_group = get_exercises_by_group(muscle_groups, exercises_by_muscle)

    # create and print workouts
    todays_workout = []
    for i in range(NUM_WORKOUTS):
        todays_workout, groups = get_todays_workout(
            muscles_by_exercise,
            exercises_by_group,
            todays_workout,
        )
        print_todays_workout(todays_workout, groups, i)


def get_todays_workout(
    muscles_by_exercise,
    exercises_by_group,
    yesterdays_workout,
):
    groups = FOCUS_MUSCLE_GROUPS
    possible_workouts = [get_workout(exercises_by_group, groups, yesterdays_workout) for _ in range(OPTIMIZATION_ATTEMPTS)]
    possible_workouts = [workout for workout in possible_workouts if workout is not None]
    todays_workout = choose_workout(possible_workouts, muscles_by_exercise)

    return todays_workout, groups


def print_todays_workout(todays_workout, groups, i):
    print(f"WORKOUT {i + 1}")
    for exercise in todays_workout:
        name, weight, reps = exercise
        print(f"{name}, {weight}s, {reps}x")
        print("1\n2\n3")
    print("\n")


def get_workout(exercises_by_group, groups, yesterdays_workout):

    def is_weight_compatible(exercise_a, exercise_b):
        weight_a = exercise_a[1]
        weight_b = exercise_b[1]

        if 50 in (weight_a, weight_b):
            return True

        if weight_a == weight_b:
            return True

        return False

    indices = [0, 1]
    random.shuffle(indices)
    group_a = groups[indices[0]]
    group_b = groups[indices[1]]

    possible_exercises_a = set(exercises_by_group[group_a])  # dedupe exercises in a group_a
    possible_exercises_a = possible_exercises_a.difference(set(yesterdays_workout))  # dedupe exercises from yesterday
    sample_a = random.sample(possible_exercises_a, EXERCISES_PER_GROUP)

    try:
        workout = []
        for exercise_a in sample_a:
            workout.append(exercise_a)

            possible_exercises_b = set(exercises_by_group[group_b])  # dedupe exercises in a group_b
            possible_exercises_b = possible_exercises_b.difference(set(yesterdays_workout))  # dedupe exercises from yesterday
            possible_exercises_b = possible_exercises_b.difference(set(sample_a))  # dedupe the whole sample even if not in workout yet
            possible_exercises_b = possible_exercises_b.difference(set(workout))  # dedupe exercises within the workout
            possible_exercises_b = [exercise_b for exercise_b in possible_exercises_b if is_weight_compatible(exercise_a, exercise_b)]  # build good exercise pairs
            exercise_b = random.choice(possible_exercises_b)
            workout.append(exercise_b)

    except IndexError:
        # these will be ignored
        return None

    else:
        return workout


def choose_workout(possible_workouts, muscles_by_exercise):
    def get_score(workout):
        score = 0

        # choose workouts that focus on similar muscles
        muscles = [muscle for exercise in workout for muscle in muscles_by_exercise[exercise]]
        muscles_set = set(muscles)
        for muscle in muscles_set:
            score += MUSCLE_FACTOR ** muscles.count(muscle)

        # choose workouts that focus on similar weights
        weights = [exercise[1] for exercise in workout]
        weights_set = set(weights)
        for weight in weights_set:
            score += WEIGHT_FACTOR ** weights.count(weight)

        for i, exercise in enumerate(workout):
            if i % 2 == 1:
                continue

            next_exercise = workout[i + 1]
            score -= PAIR_FACTOR ** len(set(exercise) & set(next_exercise))

        return score

    todays_workout = None
    score = float("-inf")
    for workout in possible_workouts:
        curr_score = get_score(workout)
        if curr_score > score:
            todays_workout = workout
            score = curr_score

    return todays_workout


def get_muscle_groups():
    df = get_df(MUSCLE_GROUPS_SHEET_NAME)

    muscle_groups = {}
    for _, row in df.iterrows():
        muscle_group = row["MUSCLE_GROUP"]
        muscles = [m.strip() for m in row["MUSCLES"].split(",")]
        muscle_groups[muscle_group] = muscles

    return muscle_groups


def get_muscles_by_exercise():
    df = get_df(EXERCISES_SHEET_NAME)

    muscles_by_exercise = {}
    for _, row in df.iterrows():
        exercise = (row["EXERCISE"], row["WEIGHT"], row["REPS"])
        muscles = [m.strip() for m in row["MUSCLES"].split(",")]
        muscles_by_exercise[exercise] = muscles

    return muscles_by_exercise


def get_df(sheet_name):
    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}")


def get_exercises_by_muscle(muscles_by_exercise):
    exercises_by_muscle = {}
    for exercise, muscles in muscles_by_exercise.items():
        for muscle in muscles:
            exercises_by_muscle[muscle] = exercises_by_muscle.get(muscle, [])
            exercises_by_muscle[muscle].append(exercise)

    return exercises_by_muscle


def get_exercises_by_group(muscle_groups, exercises_by_muscle):
    exercises_by_group = {}
    for group, muscles in muscle_groups.items():
        exercises_by_group[group] = exercises_by_group.get(group, [])
        for muscle in muscles:
            exercises = exercises_by_muscle.get(muscle, [])
            exercises_by_group[group].extend(exercises)

    return exercises_by_group


arms()
