#!/usr/bin/env python

import csv

INCIDENT_FIELDS = [
    "Incident_ID",
    "Month",
    "Day",
    "Year",
    "Date",
    "School",
    "Victims_Killed",
    "Victims_Wounded",
    "Number_Victims",
    "Shooter_Killed",
    "Source",
    "Number_News",
    "Media_Attention",
    "Reliability",
    "Quarter",
    "City",
    "State",
    "School_Level",
    "Location",
    "Location_Type",
    "During_Classes",
    "Time_Period",
    "First_Shot",
    "Duration_min",
    "Summary",
    "Narrative",
    "Situation",
    "Targets",
    "Accomplice",
    "Accomplice_Narrative",
    "Hostages",
    "Barricade",
    "Officer_Involved",
    "Bullied",
    "Domestic_Violence",
    "Gang_Related",
    "Active_Shooter_FBI",
    "Shots_Fired",
    "LAT",
    "LNG",
    "Involves_Students_Staff",
]

VICTIM_FIELDS = [
    "Incident_ID",
    "Injury",
    "Gender",
    "School_Affiliation",
    "Age",
    "Race",
]

SHOOTER_FIELDS = [
    "Incident_ID",
    "Age",
    "Gender",
    "Race",
    "School_Affiliation",
    "Shooter_Outcome",
    "Shooter_Died",
    "Injury",
]

WEAPON_FIELDS = [
    "Incident_ID",
    "Weapon_Type",
    "Weapon_Caliber",
    "Weapon_Details",
]


def clean(
    infile: str,
    fieldnames: list[str],
    incident_data: list[dict] | None = None,
):
    incident_ids = set(row['Incident_ID'] for row in incident_data) if incident_data else None
    bad_ids = []

    with open(infile) as fp:
        reader = csv.DictReader(fp)
        data = [row for row in reader]

    clean_data = []
    for row in data:
        clean_row = {}
        for key, value in row.items():
            if not key:
                continue

            clean_value = value.strip()

            if not clean_value or clean_value in {"N/A", "Unknown"}:
                clean_value = ""

            if clean_value.upper() == "YES":
                clean_value = "true"

            if clean_value.upper() == "NO":
                clean_value = "false"

            if key == "Date" and clean_value:
                month, day, year = clean_value.split("/")
                clean_value = f"{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}"

            if "Incident_ID" in key:
                clean_row["Incident_ID"] = clean_value
            else:
                clean_row[key] = clean_value

        if not any(clean_row.values()):
            continue

        if incident_ids and clean_row["Incident_ID"] not in incident_ids:
            bad_ids.append(clean_row["Incident_ID"])
            continue

        extra = set(clean_row) - set(fieldnames)
        assert not extra, extra

        missing = set(fieldnames) - set(clean_row)
        assert not missing, missing

        clean_data.append(clean_row)

    name, ext = infile.split(".")
    clean_file = ".".join([name + "_clean", ext])
    with open(clean_file, "w") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clean_data)

    print(f"{infile=} {bad_ids=}")

    return clean_data


incident_data = clean("incidents.csv", INCIDENT_FIELDS)
clean("victims.csv", VICTIM_FIELDS, incident_data=incident_data)
clean("shooters.csv", SHOOTER_FIELDS, incident_data=incident_data)
clean("weapons.csv", WEAPON_FIELDS, incident_data=incident_data)
