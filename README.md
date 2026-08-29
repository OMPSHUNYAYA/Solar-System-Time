# 🌌 Solar System Time

## Recovering historical epochs from outer-planet astrometry — a bounded reference implementation

Explore the Solar System as a live structural clock with visible planetary motion and accelerated time.

![Solar System Time](https://img.shields.io/badge/Solar%20System%20Time-Epoch%20recovery%20from%20planetary%20positions-black)
![Package](https://img.shields.io/badge/Scientific%20Package-v1.0.4-blue)
![Reference resolver](https://img.shields.io/badge/Reference%20Resolver-Python%20Stdlib-blueviolet)
![Self-test](https://img.shields.io/badge/Resolver%20Self--Test-9%2F9%20PASS-brightgreen)
![Integrity check](https://img.shields.io/badge/Ledger%20%26%20Artifact%20Integrity-17%2F17%20PASS-brightgreen)
![Clock structure check](https://img.shields.io/badge/Clock%20Structure%20Check-33%2F33%20PASS-brightgreen)
![Independent reproduction](https://img.shields.io/badge/Independent%20Third--Party%20Reproduction-OPEN%20%2F%20NOT%20YET%20CONFIRMED-orange)
![Shunyaya](https://img.shields.io/badge/Part%20of-Shunyaya%20Framework-gold)

[![Verify](https://github.com/OMPSHUNYAYA/Solar-System-Time/actions/workflows/verify.yml/badge.svg)](https://github.com/OMPSHUNYAYA/Solar-System-Time/actions/workflows/verify.yml)


---

🌐 **Live Demo:** [**Launch Solar System Clock**](https://ompshunyaya.github.io/Solar-System-Time/04_Interactive_Clock/Solar_System_Clock_v1_0_4.html)

---

**What the check badges mean**

- **Resolver Self-Test 9/9 PASS** — synthetic round-trip and resolver safeguard checks.
- **Ledger & Artifact Integrity 17/17 PASS** — shipped files, hashes, and declared fields are consistent.
- **Clock Structure Check 33/33 PASS** — declared offline HTML, interface, and responsive/mobile structure checks pass.

**These are software and package integrity checks, not independent scientific validation of the observational results.**

---

## What this is

Given the observed sky positions (right ascension and declination) of the outer
planets, the epoch of the observation can be recovered by searching for the Julian
date whose modelled planetary geometry best matches the observation. This works
because a geocentric direction to an outer planet carries two independent time
signals at once: Earth's annual orbital motion fixes the epoch within a year
(parallactic phase), and the slow secular drift of Uranus (~84 yr) and Neptune
(~165 yr) fixes which year, within a declared search window.

This is an established idea in celestial mechanics — the same principle used to date
historical astronomical records. **This package does not claim it as a new
discovery.** What the package contributes is a *clean, dependency-free reference
implementation*, a *bounded and honestly-scoped set of blind-reserve tests on real
archives*, and a *reproducible demonstration* that the inverse (position → epoch)
resolves stably within a declared window.

```text
forward:  epoch                      -> Solar-System geometry
inverse:  observed planetary sky pos -> bounded historical epoch   (this package)
```

---

## Status at a glance

The package reports a **bounded observational epoch-reconstruction result** under its
own declared protocols. Two real astrometric archives were used as blind reserves:

| Observation route | Blind cases | Result | Median absolute error |
|---|---:|---:|---:|
| USNO W1J00/W2J00 transit-circle | 24 | 24/24 within 3 days | ~0.83 day |
| Ukrainian photographic Uranus/Neptune | 7 | 7/7 within ~4 hours | ~0.15 day (~3.6 h) |

The two observational routes are not directly comparable in precision: they use different
observables, geometry, and information content, so their reported epoch errors should
not be interpreted as an instrument-precision ranking.

For the second route the seven predictions were committed before truth reveal, and a
post-blind audit widened the search interval from ~27.5 to ~82.5 years without moving
the solutions out of their basin.

**Two honest limits sit on top of these numbers:**

1. **This is a project-reported result, not an externally endorsed or
   certified one.** Independent
   third-party reproduction status is `OPEN / NOT YET CONFIRMED`.
2. **The headline numbers are not reproducible from this package alone.** The
   observational inputs are not redistributed (see Third-Party Notices). The only
   runnable computation here is the synthetic self-test, which validates the solver,
   not the model's fidelity to the real sky. One fully worked real example is on the
   roadmap so that at least one headline-style result can be checked end-to-end.

See [Scientific Status](./SCIENTIFIC_STATUS.txt) and
[Claim Boundaries](./CLAIM_BOUNDARIES.txt) for the exact interpretation.

---

## What is deliberately *not* claimed

- No replacement of UTC, TAI, GPS/GNSS, atomic clocks, or any civil/metrological timing.
- No navigation-grade, sub-second, or all-epoch reconstruction.
- No ephemeris-free method: the resolver uses published low-complexity orbital elements
  (valid ~1800–2050) and light-time-corrected astrometric directions.
- No external certification, peer review, or completed independent reproduction.
- Catalogue timestamps were used *upstream* to group near-simultaneous observations and
  to define the development/reserve split; the inverse resolver itself did not receive
  absolute epochs or within-packet time offsets.

---

## Model accuracy notes

- **Orbital elements** are the NASA/JPL approximate set valid ~1800–2050. The
  JPL **EM Bary** row is used as the compact observer-orbit proxy; the resolver
  does not model the Earth-Moon-barycenter-to-geocenter displacement. The
  higher-order correction terms for the outer planets (JPL's 3000 BC–3000 AD
  table) are not applied. The active resolver refuses searches outside
  ~1800–2050 by default; an explicit exploratory override is required.
- **Light-time** (~2.5 h to Uranus, ~4 h to Neptune) is corrected in the reference
  resolver via retarded-time iteration. The correction removes a known geometric omission; its effect on the historical reserve metrics is not re-scored in this package because the raw reserve inputs are not redistributed.
- For this **J2000/ICRF astrometric-coordinate contract**, no stellar-aberration
  or equator/equinox-of-date transformation is applied. Horizons' Earth-based
  apparent-coordinate output uses additional apparent-position corrections.
- A one-page **[model and error budget](./MODEL_AND_ERROR_BUDGET.txt)** separates approximate-element accuracy, light-time, coordinate contract, search-grid granularity, and observational uncertainty.

---

## Core idea

The planets are not separate clocks displayed side by side. In the project's
bounded Uranus/Neptune photographic test, their combined observed geometry
resolved epochs to hour-scale error within the declared search window. This
package makes that inverse relation explicit, bounded, and inspectable.

*Part of the Shunyaya Framework.*

---

## Repository map

- [`01_Reference_Implementation/`](./01_Reference_Implementation/) — dependency-free inverse resolver
- [`02_Frozen_Evidence/`](./02_Frozen_Evidence/) — evidence ledger and observational evidence summary
- [`03_Verification/`](./03_Verification/) — ledger/key-artifact integrity verifier and SHA-256 manifest
- [`04_Interactive_Clock/`](./04_Interactive_Clock/) — standalone Solar System Clock and structure verifier

## Active files

- [`Solar_System_Time_Reference_Resolver_v1_0_4.py`](./01_Reference_Implementation/Solar_System_Time_Reference_Resolver_v1_0_4.py) — reference inverse resolver
- [`Solar_System_Time_Evidence_Ledger_v1_0_4.json`](./02_Frozen_Evidence/Solar_System_Time_Evidence_Ledger_v1_0_4.json) — bounded project evidence ledger
- [`OBSERVATIONAL_EVIDENCE_SUMMARY.txt`](./02_Frozen_Evidence/OBSERVATIONAL_EVIDENCE_SUMMARY.txt) — compact observational record summary
- [`Solar_System_Time_Evidence_Verifier_v1_0_4.py`](./03_Verification/Solar_System_Time_Evidence_Verifier_v1_0_4.py) — **ledger/artifact integrity only**
- [`PACKAGE_ARTIFACT_SHA256SUMS_v1_0_4.txt`](./03_Verification/PACKAGE_ARTIFACT_SHA256SUMS_v1_0_4.txt) — selected key-artifact SHA-256 manifest
- [`Solar_System_Clock_v1_0_4.html`](./04_Interactive_Clock/Solar_System_Clock_v1_0_4.html) — standalone interactive clock
- [`Solar_System_Clock_v1_0_4_Verifier.py`](./04_Interactive_Clock/Solar_System_Clock_v1_0_4_Verifier.py) — **HTML/offline/UI structure only**
- [`SCIENTIFIC_STATUS.txt`](./SCIENTIFIC_STATUS.txt) — current bounded scientific status
- [`CLAIM_BOUNDARIES.txt`](./CLAIM_BOUNDARIES.txt) — explicit claim limits
- [`MODEL_AND_ERROR_BUDGET.txt`](./MODEL_AND_ERROR_BUDGET.txt) — model scope and error-budget notes
- [`EXTERNAL_TIMESTAMP_STATUS.txt`](./EXTERNAL_TIMESTAMP_STATUS.txt) — chronology/timestamp status
- [`REAL_WORKED_EXAMPLE_STATUS.txt`](./REAL_WORKED_EXAMPLE_STATUS.txt) — worked-example status and roadmap
- [`LICENSE`](./LICENSE) — package license map
- [`THIRD_PARTY_NOTICES.txt`](./THIRD_PARTY_NOTICES.txt) — source and rights notices

The evidence ledger records `R8E...CLAIM_AUDIT_PASS` as a historical project
record. It is not the current package status and does not imply outside
endorsement, certification, peer review, or independent validation.

## Quick verification

```text
python -B 01_Reference_Implementation/Solar_System_Time_Reference_Resolver_v1_0_4.py --self-test
python -B 03_Verification/Solar_System_Time_Evidence_Verifier_v1_0_4.py --verify
python -B 04_Interactive_Clock/Solar_System_Clock_v1_0_4_Verifier.py
```

The first command validates synthetic solver behavior. The second validates
ledger consistency and the selected key-artifact manifest. The third validates
HTML structure/offline properties.
**None of the three commands reproduces the historical blind observational
metrics.**

## Interactive clock

The bundled [Solar System Clock v1.0.4](./04_Interactive_Clock/Solar_System_Clock_v1_0_4.html) remains a standalone, dependency-free
visual reference/demo. It opens at **30 days/second** for immediate visible
planetary motion; **NOW** returns to current UTC at 1x. The display is explicitly
labelled **LOW-PRECISION ORBITAL MODEL** so it cannot reasonably be mistaken for
a precision ephemeris.

## License

- Software and verification code: **[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)**
- Project-authored documentation: **[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)**
- Third-party materials remain subject to their respective terms.

See [`LICENSE`](LICENSE) and [`THIRD_PARTY_NOTICES.txt`](THIRD_PARTY_NOTICES.txt).

## Reproduction priority

The highest-value next scientific improvement is not another green package
check. It is a **new, independently traceable real-observation reproduction**
with externally timestamped pre-truth predictions and redistributable/minimal
inputs where source rights permit.
