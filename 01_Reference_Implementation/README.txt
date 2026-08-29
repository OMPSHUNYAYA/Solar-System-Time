SOLAR SYSTEM TIME REFERENCE IMPLEMENTATION v1.0.4

Entry point:
Solar_System_Time_Reference_Resolver_v1_0_4.py

Self-test:
python -B Solar_System_Time_Reference_Resolver_v1_0_4.py --self-test

Purpose
-------
Compact Python-standard-library reference implementation for bounded recovery
of an observation epoch from J2000 astrometric Uranus/Neptune RA/Dec.

Reference model
---------------
- retarded-time planetary light-time correction is enabled by default;
- stellar aberration is intentionally not applied to the J2000 astrometric lane;
- RA/Dec input validation is explicit;
- searches outside the declared 1800-2050 validity interval of the approximate
  JPL element set are refused by default;
- --allow-outside-model-validity permits clearly marked exploratory use only.

The one-day coarse sweep is intentionally simple and O(N) in the declared
search span. Very wide exploratory windows are not the intended operating mode.

This is a reference implementation, not a civil-time, metrological, navigation,
or unrestricted all-time timing system.

Model notes
-----------
- the JPL Table-1 EM-Bary row is used as the compact observer-orbit proxy;
- Earth-Moon-barycenter-to-geocenter displacement is not modelled;
- the supplied Julian-date coordinate is used directly; explicit UTC/UT1 <->
  TDB conversion is outside this compact reference implementation;
- the declared validity guard admits the full calendar interval 1800 through
  2050 and rejects the exclusive boundary at 2051-01-01 00:00.
