# SOLAR SYSTEM TIME JOURNEY (SSTJ) v1.5.3

Solar System Time Journey (SSTJ) is a self-contained browser application that combines a live or simulated low-precision Solar System clock with a moving-observer Journey layer for Walk, Run, and Ride activity.

---

## Application

[`Solar_System_Time_Journey_v1_5_3.html`](./Solar_System_Time_Journey_v1_5_3.html)

Solar System Time Journey is provided as a standalone HTML application.

Move across Earth while seeing how far Earth carries you through the Solar System.

For live browser-geolocation use on a supported mobile browser:

- allow Location access
- use outdoors for the most reliable location signal
- select Walk / Run / Ride and km / miles
- tap START LIVE JOURNEY
- begin moving when Journey Signal reaches `GOOD` or `EXCELLENT`
- distance and estimated steps are derived from accepted location movement and may update in batches rather than once per physical step
- temporary location-quality or acquisition gaps can pause qualified ground-distance accumulation
- when usable location acquisition recovers, qualified distance and estimated steps can resume without bridging across an unqualified interval
- Ride does not report steps
- use Pause / Resume when needed
- tap END JOURNEY to seal the Journey

`WAITING` or `LOCATION-DISTANCE PAUSED` means SSTJ is waiting for a usable location state.

---

## Core relations

`time -> planetary state -> structural timestamp`

`time + observer position + motion -> Solar System place-time journey record`

`observer motion != change to planetary clock state`

SSTJ v1.5.3 extends the measurement-qualified Journey architecture with explicit kilometre/mile presentation control, bounded location-acquisition assistance, freshness-aware Journey Signal states, qualified sub-noise movement accumulation, and recovery from stalled accepted-ground progress while preserving canonical metric geometry, scientific boundaries, privacy, and integrity semantics.

---

## Main capabilities

- live UTC planetary clock
- accelerated planetary time
- Mercury-through-Neptune heliocentric visualization
- explicit 1800-2050 approximate-element guardrail
- live browser-geolocation Journey recording
- bounded fresh-position assistance after sustained callback silence, sustained lack of distance-qualified accuracy, or stalled accepted-ground progress
- freshness-aware Journey Signal so an old accurate fix cannot remain indefinitely presented as a current excellent state
- qualified sub-noise movement accumulation against a stable distance anchor
- continuity-safe recovery without bridging across unqualified location intervals
- final fresh-position acquisition attempt before sealing a live Journey
- synthetic Demo mode without location permission
- Walk / Run / Ride activity modes
- configurable Walk/Run stride frozen at Journey start
- automatic landing-screen preference:
  - Automatic: Planet View on desktop, Journey View on mobile
  - explicit Planet View override
  - explicit Journey View override
- browser-local Journey distance-unit preference:
  - Kilometres
  - Miles
  - canonical geometry and exported scientific quantities remain metric
- optional distance or active-time Journey goal
- manual Pause / Resume without cross-pause route bridging
- automatic Solar Splits using the unit frozen at Journey start:
  - Walk/Run: 1 km or 1 mile
  - Ride: 5 km or 5 miles
- live Journey Signal for current measurement state
- browser-session continuity event record
- compact Recent Journey summaries stored only in browser local storage
- WGS84 ellipsoidal ground-distance calculation
- accuracy-relative motion qualification
- timestamp freshness and non-monotonic timestamp diagnostics
- activity-aware segment-speed filtering
- raw-coordinate-path and qualified-ground-path separation
- route directness when the qualified path is continuous
- browser-reported horizontal-accuracy median and p95 summaries
- measurement-quality grade based on declared browser-reported quality rules
- observed-data and derived-data separation in exported breadcrumbs
- explicit segment qualification reason codes
- browser capability coverage for speed, heading, altitude, and altitudeAccuracy
- altitudeAccuracy-qualified elevation gain/loss
- approximate Earth-rotation carriage
- approximate Earth-orbit carriage
- Cosmic Breadcrumbs with fixed-cap retention
- append-only SHA-256 breadcrumb hash chain
- final SHA-256 record digest
- JSON export
- local route trace without external map tiles
- Content Security Policy and no-referrer policy
- no fetch/XHR/WebSocket/EventSource/sendBeacon runtime path
- reduced-motion and keyboard/focus accessibility handling
- Screen Wake Lock request/re-acquisition when supported

---

## Landing-screen preference

The default preference is Automatic.

Automatic resolves as:

`desktop -> Planet View`

`mobile -> Journey View`

The user can explicitly select Planet View or Journey View as the default for that browser.

The preference is stored with browser local storage. It is not sent to a server and does not require an account.

The responsive decision boundary used by Automatic is a browser viewport width of 760 CSS pixels.

---

## Distance-unit preference

The Journey distance-unit preference is browser-local and can be set to:

Kilometres

Miles

The preference controls user-facing Journey distance, speed, pace, distance goals, Solar Splits, Earth-motion distance display, and Recent Journey distance display.

Canonical internal geometry remains metric:

`canonical_distance_unit = km`

`canonical_length_unit = m`

The exact conversion is:

`1 mi = 1.609344 km`

`mi = km / 1.609344`

`km = mi * 1.609344`

The unit in effect at Journey start is frozen for interpreting a declared distance goal and selecting round Solar Split milestones. The preference selector is locked while a Journey is active.

Changing the browser display preference after a Journey ends does not change canonical route geometry, breadcrumbs, the Journey-start unit declaration, or the sealed record digest.

Short metric distances can display in metres. Short mile-mode distances can display in feet. Accuracy, altitude, altitudeAccuracy, and stride declarations remain in metres because they are measurement/provenance quantities rather than the Journey distance presentation layer.

---

## Journey goals

A Journey can start with no goal, a distance goal, or an active-time goal.

Distance goal input range in the selected display unit:

`0.1 <= distance_goal_display <= 1000`

A distance goal is converted once at Journey start:

`distance_goal_km = distance_goal_display                          [kilometre mode]`

`distance_goal_km = distance_goal_display * 1.609344             [mile mode]`

The canonical goal comparison is:

`goal_progress = qualified_ground_path_km / distance_goal_km`

Time goal range:

`1 min <= time_goal <= 1440 min`

The selected goal is frozen at Journey start.

The declared distance value/unit and canonical kilometre value are preserved separately in the Journey record.

Time goals use active Journey time:

`active_time = wall_elapsed_time - manual_paused_time`

The goal is a project-defined Journey milestone. It is not a medical, training, or physiological prescription.

---

## Pause / Resume model

Manual Pause is an observer-recording control.

On Pause:

- live geolocation acquisition or Demo generation stops
- the pre-pause segment anchor is cleared
- the elevation anchor is cleared
- the Screen Wake Lock is intentionally released when held
- manual paused time begins accumulating
- the planetary clock and physical elapsed time continue

On Resume:

- manual paused time is finalized
- a fresh route anchor is required
- no ground-distance segment is drawn across the pause
- live acquisition or Demo generation restarts
- Screen Wake Lock is requested again when supported

Therefore:

`manual_pause != pause of physical time`

`manual_pause != pause of Earth rotation`

`manual_pause != pause of Earth orbit`

`manual_pause != pause of planetary state`

---

## Solar Splits

Automatic distance milestones use the distance unit frozen at Journey start:

Kilometre mode:

Walk: 1 km

Run: 1 km

Ride: 5 km

Mile mode:

Walk: 1 mi

Run: 1 mi

Ride: 5 mi

Canonical split thresholds are stored in kilometres. Therefore:

`1 mi split = 1.609344 km`

`5 mi split = 8.04672 km`

When an accepted WGS84 segment crosses one or more split thresholds, SSTJ interpolates the milestone fraction within that accepted segment.

For a target split at cumulative distance D_target:

`f = (D_target - D_before) / segment_distance`

with:

`0 <= f <= 1`

The split UTC and approximate position are interpolated at that fraction.

Each Solar Split records:

- split number
- cumulative qualified ground distance
- split distance
- UTC
- interpolated approximate latitude/longitude
- cumulative active time
- split active time
- approximate split pace for Walk/Run
- approximate split average speed
- contemporaneous planetary state
- associated breadcrumb-chain SHA-256 value

A Solar Split is a project-derived milestone. It is not an independent sensor observation.

---

## Journey Signal

The live Journey Signal provides a compact view of current recording conditions.

Possible states include:

- EXCELLENT
- GOOD
- LIMITED
- WAITING
- PAUSED
- SYNTHETIC
- SEALED

For live browser-geolocation fixes, the current reported horizontal accuracy contributes to the signal:

`EXCELLENT: accuracy <= 8 m`

`GOOD: 8 m < accuracy <= 15 m`

`LIMITED: 15 m < accuracy <= 35 m`

`WAITING: no current distance-qualified fix`

These are project-defined interface states, not calibrated probabilities of true positional error.

Location fixes are delivered by the browser/device location provider and can arrive intermittently or with delay. Journey Signal therefore considers both reported location quality and acquisition freshness. A previously accurate fix does not remain indefinitely classified as a current excellent state when fresh location callbacks stop. Journey Signal is not a promise of continuous real-time location-update cadence.

---

## Continuity state

A browser application can be affected by page visibility, background suspension, geolocation delivery gaps, and Screen Wake Lock lifecycle changes.

SSTJ records observable continuity events including:

- page hidden
- page visible
- geolocation gap
- Screen Wake Lock lost
- Screen Wake Lock reacquired

A live geolocation callback gap is counted when:

`callback_gap_ms > 15000`

Continuity reporting describes conditions observable by the page. It does not prove that no operating-system suspension occurred outside browser-observable events.

---

## Recent Journeys

SSTJ can retain up to 20 compact completed-Journey summaries in browser local storage.

A Recent Journey summary can include:

- start/end UTC
- Demo or live mode
- activity
- qualified ground distance
- active time
- wall elapsed time
- manual paused time
- estimated steps when applicable
- approximate average pace when applicable
- measurement-quality grade
- goal type/value/achievement state
- Solar Split count
- record SHA-256

Recent Journey summaries intentionally do not store:

- route coordinates
- breadcrumb arrays
- full planetary breadcrumb history

The full Journey record persists only when the user explicitly exports JSON.

Browser local storage can be cleared by the user, browser, operating system, privacy mode, storage policy, or site-data management.

---

## Ground-distance model

Qualified ground distance uses a project-authored implementation of the WGS84 ellipsoidal Vincenty inverse solution.

`WGS84_A_KM = 6378.137`

`WGS84_F = 1 / 298.257223563`

`WGS84_B_KM = WGS84_A_KM * (1 - WGS84_F)`

For a qualified coordinate pair:

`ground_segment = WGS84_VINCENTY_INVERSE(point_a, point_b)`

If the Vincenty inverse iteration does not converge, SSTJ falls back to the mean-radius haversine model:

`MEAN_EARTH_RADIUS_KM = 6371.0088`

`ground_segment_fallback = mean_radius_haversine(point_a, point_b)`

Fallback use is counted in the exported measurement-quality block.

The synthetic Demo destination step uses the corresponding WGS84 Vincenty direct solution.

---

## Distance qualification

A live browser-geolocation fix can become distance-qualified only when:

`reported_horizontal_accuracy_m <= 35`

and:

`position_age_ms <= 90000`

A rejected fix may still be displayed and retained, but it does not contribute qualified ground distance and breaks path continuity. The next qualified fix does not bridge across that rejected interval.

For two consecutive qualified live fixes, SSTJ also applies an accuracy-relative positional-noise threshold:

`pair_accuracy_m = hypot(previous_accuracy_m, current_accuracy_m)`

`motion_signal_min_ratio = 0.5`

`positional_noise_threshold_m = max(2, min(25, motion_signal_min_ratio * pair_accuracy_m))`

A segment must meet or exceed that threshold before it can contribute qualified distance.

A qualified movement that is individually below the positional-noise threshold is not immediately counted as ground distance. Instead, SSTJ can retain the last qualified distance anchor and allow successive qualified sub-noise movement to accumulate against that stable anchor for a bounded interval. If the accumulated movement subsequently satisfies the declared positional-noise and other segment gates, the resulting qualified segment can contribute ground distance.

An unqualified fix breaks this continuity and clears the relevant distance anchor. SSTJ does not bridge qualified ground distance across an unqualified interval.

Activity-aware maximum segment speeds are:

Walk: 15 m/s

Run: 25 m/s

Ride: 120 m/s

Ride is intended for ground travel. SSTJ is not an aviation tracker.

---

## Segment reason codes

Each retained breadcrumb records the qualification state of the segment arriving at that breadcrumb.

Principal states are:

- FIRST_FIX
- ACCEPTED
- REJECTED_UNQUALIFIED_FIX_PAIR
- REJECTED_STALE_TIMESTAMP
- REJECTED_NONPOSITIVE_DT
- REJECTED_INTERVAL_TOO_SHORT
- REJECTED_TOO_SMALL_FOR_POSITIONAL_NOISE
- REJECTED_IMPLAUSIBLE_SPEED

This makes:

`raw fixes -> declared gates -> qualified trajectory`

auditable from the exported record.

---

## Raw and qualified paths

SSTJ preserves two distinct path quantities.

`raw_coordinate_path_km`

This is the sum of positive-time coordinate-to-coordinate WGS84 distances before distance-quality filtering. It is retained as diagnostic provenance and can include substantial location noise.

`ground_path_km`

This is the headline qualified path after the declared fix and segment gates.

The two values are intentionally not interchangeable.

---

## Route directness

When the qualified path is continuous:

`route_directness_ratio = distance_from_start / qualified_ground_path`

A loop can legitimately have low directness.

If a rejected fix breaks qualified-path continuity, route directness is reported as unavailable rather than presenting a potentially misleading ratio.

---

## Measurement-quality state

SSTJ reports browser-reported horizontal-accuracy summaries instead of inventing a cumulative route-distance confidence interval.

The exported quality block includes:

- quality_grade
- browser_reported_horizontal_accuracy_median_m_approx
- browser_reported_horizontal_accuracy_p95_m_approx
- rejected_fix_fraction
- fixes_received
- fixes_distance_qualified
- fixes_rejected_accuracy
- fixes_rejected_temporal
- stale_fix_count
- nonmonotonic_timestamp_count
- provider_timestamp_fallback_count
- geodesic_fallback_count
- segments_accepted
- segments_rejected
- segment rejection counts by reason family

The accuracy quantiles use a compact streaming histogram and are approximate to the histogram resolution.

The quality grade is a project-defined summary of browser-reported measurement conditions. It is not a guarantee of true physical position error.

---

## Observed and derived data

Exported breadcrumbs separate browser/device observations from project-derived quantities.

Observed examples:

- latitude
- longitude
- altitude
- horizontal accuracy
- altitude accuracy
- browser-reported speed
- browser-reported heading
- provider timestamp
- callback wall time
- callback monotonic time

Derived examples:

- position age
- temporal qualification
- distance qualification
- segment state
- WGS84 segment distance
- qualified segment distance
- positional-noise threshold
- motion-signal ratio
- resolved speed
- resolved heading
- contemporaneous planetary display fingerprint

This distinction allows a verifier to determine what the browser supplied and what SSTJ computed.

---

## Browser capability variability

The browser Geolocation API does not guarantee a specific positioning technology.

Depending on browser, hardware, permission state, and positioning source, speed, heading, altitude, or altitudeAccuracy may be unavailable.

SSTJ records capability coverage. Where declared, it falls back to derived values; otherwise the quantity is reported as unavailable.

The application therefore uses the term browser geolocation for the measurement source rather than asserting that every fix is GNSS/GPS-derived.

---

## Timestamp model

Each live fix can preserve:

- provider_timestamp_ms
- callback_wall_ms
- callback_monotonic_ms
- position_age_ms

A provider timestamp older than 90 seconds is not distance-qualified.

A non-positive interval between consecutive provider timestamps cannot contribute ground distance.

Long positive intervals over 90 seconds are classified as unclassified time even when an otherwise valid spatial segment is retained.

---

## Fitness metrics

For Walk and Run:

`estimated_steps = qualified_ground_distance_m / declared_stride_length_m`

Default stride values:

Walk: 0.78 m per step

Run: 1.05 m per step

Ride: not applicable

User-declared Walk/Run stride range:

`0.30 m <= stride <= 2.50 m`

The stride in effect when a Journey starts is frozen into that Journey.

The result is an estimate and is not a sensor-measured pedometer count.

Distance and estimated steps are derived from accepted location updates and therefore can appear with browser/device location-provider delay rather than changing continuously every second.

Average moving speed is:

`average_moving_speed = qualified_ground_distance / moving_time`

Average Walk/Run pace is:

`average_pace = moving_time / qualified_ground_distance`

Elevation requires altitude and altitudeAccuracy-qualified counted segments.

---

## Earth-motion carriage

Approximate Earth-rotation carriage uses a WGS84 spin-axis-radius model at mean distance-qualified latitude.

Approximate Earth-orbit carriage uses the low-precision Earth orbital model used by the planetary clock.

Both are derived from wall elapsed Journey time, including manual-pause intervals, because physical Earth motion does not pause when Journey acquisition pauses.

These values are not added to ground distance.

---

## Breadcrumb integrity

Each Journey initializes a chain genesis value from a canonical Journey header.

`H_0 = SHA256(journey_chain_header)`

For each breadcrumb n:

`H_n = SHA256(H_(n-1) || canonical_breadcrumb_n)`

The completed Journey records the final chain root.

The detailed breadcrumb store retains up to:

`MAX_BREADCRUMBS = 5000`

When older breadcrumbs are summarized by the circular retention policy, the retained suffix preserves its prior-chain anchor so that the retained suffix can still be independently recomputed.

The hash chain provides tamper evidence for recorded breadcrumb ordering/content.

`breadcrumb SHA-256 chain != proof of presence`

`breadcrumb SHA-256 chain != proof of location authenticity`

---

## Record digest

A completed Journey receives a SHA-256 digest over the canonical exported record before the digest field is attached.

The implementation prefers the browser Web Crypto SHA-256 implementation and includes a self-contained SHA-256 fallback.

`record SHA-256 != proof of presence`

`record SHA-256 != proof of location authenticity`

`record SHA-256 != proof that browser geolocation was genuine`

---

## Integrity manifest scope

`SHA256SUMS.txt` intentionally covers only the two executable artifacts:

- `Solar_System_Time_Journey_v1_5_3.html`
- `Solar_System_Time_Journey_v1_5_3_Verifier.py`

Documentation, scientific-boundary, provenance, copyright, and license files are deliberately not included in the checksum manifest. Their repository history remains visible through version control, while executable-artifact integrity can be checked without forcing checksum changes for documentation-only edits.

---

## Privacy and network posture

The application is self-contained.

It includes no external JavaScript, map tiles, remote stylesheets, remote fonts, images, or analytics runtime.

The application contains no fetch, XMLHttpRequest, WebSocket, EventSource, or sendBeacon runtime path.

Browser geolocation is used only after the user starts a live Journey and grants the required permission.

Recent Journey summaries, landing preference, and the distance-unit preference use browser local storage only.

---

## Location acquisition

Live geolocation is designed for a secure top-level HTTPS browser context.

The application provides location-assistance messages for blocked permissions, unsupported browser contexts, embedded contexts, unavailable fixes, and device/browser location settings where supported.

SSTJ keeps the browser `watchPosition()` stream as the primary live acquisition path. A bounded, rate-controlled fresh-position request can also be used when there is sustained callback silence, sustained absence of distance-qualified accuracy, or sustained absence of accepted ground progress.

Acquisition assistance does not bypass horizontal-accuracy, timestamp-freshness, positional-noise, continuity, or activity-speed qualification.

When a live Journey is ended, SSTJ can attempt one final fresh high-accuracy position before sealing the record. Failure to obtain that final position does not prevent the existing Journey from being sealed.

A local file is not treated as the primary live-geolocation deployment environment.

Indoor or obstructed conditions can produce unavailable, intermittent, or delayed usable location fixes. Qualified ground distance is intentionally allowed to pause under such conditions rather than counting unqualified location movement.

---

## Verification

From the package directory:

`python -B Solar_System_Time_Journey_v1_5_3_Verifier.py`

The browser application also includes an embedded runtime self-test.

Open the HTML, open the browser console, and run:

```javascript
(async()=>{
  const r=await runSSTJSelfTest();
  console.log(r.status, r.passed+"/"+r.total);
  console.table(r.checks);
})();
```

The v1.5.3 embedded self-test contains 59 checks covering planetary-state guards, WGS84 geometry, distance qualification, integrity, retention, provenance, landing preference, kilometre/mile conversion, Solar Splits, active-time pause accounting, Journey Signal states, callback-wall provenance, continuity handling, acquisition-assist controls, accepted-progress stall detection, signal-freshness aging, qualified sub-noise movement accumulation, and prevention of route bridging across unqualified or paused intervals.

Package verification and browser self-tests are not substitutes for real-device field validation.

Field-level validation across multiple devices, browsers, operating systems, movement patterns, and positioning conditions is ongoing.

Estimated steps are derived from qualified ground distance and the declared stride length. They are not sensor-measured pedometer steps and may update in batches as accepted location segments become available.

Location availability and quality can vary with device, browser, environment, and positioning conditions. SSTJ intentionally avoids counting unqualified movement and does not bridge qualified ground distance across unqualified intervals.

---

## Scientific boundary

SSTJ is a project-defined measurement-qualified place-time Journey representation layered over a low-precision Solar System clock.

It is not:

- a precision ephemeris
- a navigation-certified geodesy product
- a medical or clinical fitness product
- a sensor-certified pedometer
- proof of physical presence
- proof of route authenticity
- proof that browser location came specifically from GNSS/GPS
- an aviation tracker

See SCIENTIFIC_BOUNDARY.txt for the complete boundary statement.

---

## Licensing and provenance

Project-authored software is governed by the Apache License, Version 2.0.

Project-authored documentation and explanatory material are governed by CC BY-NC 4.0 unless a file states otherwise.

Third-party facts, standards, services, names, and source material remain subject to their applicable rights and terms.

See LICENSE, COPYRIGHT_NOTICE.txt, and THIRD_PARTY_NOTICES.txt.
