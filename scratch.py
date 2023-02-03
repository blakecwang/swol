#!/usr/bin/env python

from datetime import datetime
import pandas as pd


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
SCHEDULE = (
    ("arms", "shoulders"),  # Monday
    ("chest", "back"),      # Tuesday
    ("arms", "shoulders"),  # Wednesday
    ("core", "legs"),       # Thursday
    ("chest", "back"),      # Friday
    ("arms", "shoulders"),  # Saturday
    ("chest", "back"),      # Sunday
)


def swol():
    # group -> muscle -> exercise
    # choose groups based on weekday
    # get all exercises for group
    #   get all muscles for each group
    #   get all exercises for each muscle

    # build convenient data structures
    #groups_by_muscle = get_groups_by_muscle()
    exercises_by_muscle = get_exercises_by_muscle(groups_by_muscle)
    breakpoint()
    exit()

    groups = get_muscle_groups()

    for group in groups:
        group_exercises = get_group_exercises(group)


    exercises_by_group = get_exercises_by_group(df)
    validate_data(df, groups_by_muscle)

    exercises = []
    # group -> muscle -> exercise
    for group in pair:
        muscles = MUSCLE_GROUPS[group]
        for i, row in df.iterrows():
            breakpoint()


    print(":)")


def get_muscle_groups():
    weekday = datetime.now().weekday()
    return SCHEDULE[weekday]


def get_exercises_by_muscle():
    SHEET_ID = "11lRtA-7zxK1OUACGokvvH60mWBB3i7--0D8jwCrCuKg"
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv")

    exercises_by_muscle = {}
    for _, row in df.iterrows():
        exercise = row["EXERCISE"]
        muscles = [m.strip() for m in row["MUSCLES"].split(",")]
        for muscle in muscles:
            exercises_by_muscle[muscle] = exercises_by_muscle.get(muscle, [])
            exercises_by_muscle[muscle].append(muscle)

    return exercises_by_muscle


def get_groups_by_muscle():
    groups_by_muscle = {}
    for group, muscles in MUSCLE_GROUPS.items():
        for muscle in muscles:
            assert muscle not in groups_by_muscle  # no duplicates
            groups_by_muscle[muscle] = group

    return groups_by_muscle


def validate_data(df, groups_by_muscle):
    for i, row in df.iterrows():
        muscles = [m.strip() for m in row["MUSCLES"].split(",") if m]
        for muscle in muscles:
            if muscle not in groups_by_muscle:
                print(f"missing '{muscle}' from '{row['EXERCISE']}'")
                exit(1)




def get_exercises_by_group(df):
    pass
#    for row in 



swol()
