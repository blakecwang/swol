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
    df = get_df()
    muscle_groups_by_muscle = get_muscle_groups_by_muscle()
    validate_data(df, muscle_groups_by_muscle)
    pair = get_pair()

    exercises = []
#    for muscle_group in pair:
#        MUSCLE_GROUPS


    print(":)")


def get_df():
    SHEET_ID = "11lRtA-7zxK1OUACGokvvH60mWBB3i7--0D8jwCrCuKg"
    return pd.read_csv(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv")


def get_muscle_groups_by_muscle():
    muscle_groups_by_muscle = {}
    for muscle_group, muscles in MUSCLE_GROUPS.items():
        for muscle in muscles:
            assert muscle not in muscle_groups_by_muscle  # no duplicates
            muscle_groups_by_muscle[muscle] = muscle_group

    return muscle_groups_by_muscle


def validate_data(df, muscle_groups_by_muscle):
    for i, row in df.iterrows():
        muscles = [m.strip() for m in row["MUSCLES"].split(",")]
        for muscle in muscles:
            if muscle not in muscle_groups_by_muscle:
                print(f"missing '{muscle}' from '{row['EXERCISE']}'")
                exit(1)

def get_pair():
    weekday = datetime.now().weekday()
    return SCHEDULE[weekday]


swol()
