--CREATE TABLE incidents (
--    Incident_ID TEXT PRIMARY KEY,
--    Month TEXT,
--    Day TEXT,
--    Year TEXT,
--    "Date" date,
--    School TEXT,
--    Victims_Killed INTEGER,
--    Victims_Wounded INTEGER,
--    Number_Victims INTEGER,
--    Shooter_Killed INTEGER,
--    Source TEXT,
--    Number_News INTEGER,
--    Media_Attention TEXT,
--    Reliability INTEGER,
--    Quarter TEXT,
--    City TEXT,
--    State TEXT,
--    School_Level TEXT,
--    Location TEXT,
--    Location_Type TEXT,
--    During_Classes BOOLEAN,
--    Time_Period TEXT,
--    First_Shot TIME,
--    Duration_min INTEGER,
--    Summary TEXT,
--    Narrative TEXT,
--    Situation TEXT,
--    Targets TEXT,
--    Accomplice BOOLEAN,
--    Accomplice_Narrative TEXT,
--    Hostages BOOLEAN,
--    Barricade BOOLEAN,
--    Officer_Involved BOOLEAN,
--    Bullied BOOLEAN,
--    Domestic_Violence BOOLEAN,
--    Gang_Related BOOLEAN,
--    Active_Shooter_FBI BOOLEAN,
--    Shots_Fired TEXT,
--    LAT DECIMAL,
--    LNG DECIMAL,
--    Involves_Students_Staff BOOLEAN
--);
--
--CREATE TABLE victims (
--    Incident_ID TEXT,
--    Injury TEXT,
--    Gender TEXT,
--    School_Affiliation TEXT,
--    Age TEXT,
--    Race TEXT,
--    FOREIGN KEY (Incident_ID) REFERENCES incidents(Incident_ID)
--);
--
CREATE TABLE shooters (
    Incident_ID TEXT,
    Age TEXT,
    Gender TEXT,
    Race TEXT,
    School_Affiliation TEXT,
    Shooter_Outcome TEXT,
    Shooter_Died BOOLEAN,
    Injury TEXT,
    FOREIGN KEY (Incident_ID) REFERENCES incidents(Incident_ID)
);

--CREATE TABLE weapons (
--    Incident_ID TEXT,
--    Weapon_Type TEXT,
--    Weapon_Caliber TEXT,
--    Weapon_Details TEXT,
--    FOREIGN KEY (Incident_ID) REFERENCES incidents(Incident_ID)
--);
