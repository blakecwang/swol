The fatality risk of sending a kid to school TK-12th is 1 in 23k.
The fatality risk of driving for same time period is 1 in 600 (38x greater).

```
\copy incidents FROM 'incidents_clean.csv' WITH (FORMAT csv, HEADER true);
\copy victims FROM 'victims_clean.csv' WITH (FORMAT csv, HEADER true);
\copy shooters FROM 'shooters_clean.csv' WITH (FORMAT csv, HEADER true);
\copy weapons FROM 'weapons_clean.csv' WITH (FORMAT csv, HEADER true);
```
