-- What is the chance of a student being killed in a school shooting
-- over the entire length of their schooling?
-- Answer: 0.0000436
select count(*) / 3300000.0 -- Number of 2024 highschool graduates
from victims v
join incidents i on v.incident_id = i.incident_id
and "Date" > (select max("Date") from incidents) - interval '14 years'
and i."Date" > '2010-09-01' -- Start TK
and i."Date" < '2024-06-30' -- Graduate highschool
where v.injury = 'Fatal'
and (
    v.school_affiliation = 'Student'
    or v.age in ('Teen', 'Child')
    or case when v.age ~ '^\d+$' then cast(v.age as integer) end < 18
)
and i.during_classes is true
