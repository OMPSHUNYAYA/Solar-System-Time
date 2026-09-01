#!/usr/bin/env python3
from pathlib import Path
import hashlib
import math
import re
import sys

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "Solar_System_Time_Journey_v1_5_0.html"
MANIFEST = ROOT / "SHA256SUMS.txt"
HASHED_ARTIFACTS = {
    "Solar_System_Time_Journey_v1_5_0.html",
    "Solar_System_Time_Journey_v1_5_0_Verifier.py",
}
REQUIRED = [
    "Solar_System_Time_Journey_v1_5_0.html",
    "Solar_System_Time_Journey_v1_5_0_Verifier.py",
    "README.md",
    "SCIENTIFIC_BOUNDARY.txt",
    "LICENSE",
    "COPYRIGHT_NOTICE.txt",
    "THIRD_PARTY_NOTICES.txt",
    "SHA256SUMS.txt",
]


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path):
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def manifest_items():
    if not MANIFEST.is_file():
        return {}
    out = {}
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or "  " not in line:
            if line:
                return {}
            continue
        digest, name = line.split("  ", 1)
        out[name] = digest
    return out


def vincenty_km(lat1, lon1, lat2, lon2, a_km, f):
    b_km = a_km * (1 - f)
    p1, p2 = math.radians(lat1), math.radians(lat2)
    L = math.radians(lon2 - lon1)
    U1, U2 = math.atan((1 - f) * math.tan(p1)), math.atan((1 - f) * math.tan(p2))
    sinU1, cosU1, sinU2, cosU2 = math.sin(U1), math.cos(U1), math.sin(U2), math.cos(U2)
    lam = L
    for _ in range(100):
        sl, cl = math.sin(lam), math.cos(lam)
        x = cosU2 * sl
        y = cosU1 * sinU2 - sinU1 * cosU2 * cl
        sin_sigma = math.hypot(x, y)
        if sin_sigma == 0:
            return 0.0
        cos_sigma = sinU1 * sinU2 + cosU1 * cosU2 * cl
        sigma = math.atan2(sin_sigma, cos_sigma)
        sin_alpha = cosU1 * cosU2 * sl / sin_sigma
        cos2_alpha = 1 - sin_alpha * sin_alpha
        cos2_sigma_m = 0 if cos2_alpha == 0 else cos_sigma - 2 * sinU1 * sinU2 / cos2_alpha
        C = f / 16 * cos2_alpha * (4 + f * (4 - 3 * cos2_alpha))
        prev = lam
        lam = L + (1 - C) * f * sin_alpha * (sigma + C * sin_sigma * (cos2_sigma_m + C * cos_sigma * (-1 + 2 * cos2_sigma_m * cos2_sigma_m)))
        if abs(lam - prev) <= 1e-12:
            break
    else:
        return None
    u2 = cos2_alpha * (a_km * a_km - b_km * b_km) / (b_km * b_km)
    A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    ds = B * sin_sigma * (cos2_sigma_m + B / 4 * (cos_sigma * (-1 + 2 * cos2_sigma_m * cos2_sigma_m) - B / 6 * cos2_sigma_m * (-3 + 4 * sin_sigma * sin_sigma) * (-3 + 4 * cos2_sigma_m * cos2_sigma_m)))
    return b_km * A * (sigma - ds)


checks = {}
for name in REQUIRED:
    checks[f"artifact:{name}"] = (ROOT / name).is_file()

manifest = manifest_items()
checks["manifest:expected_entries"] = set(manifest) == HASHED_ARTIFACTS
checks["manifest:documentation_unhashed"] = not any(name in manifest for name in {"README.md", "SCIENTIFIC_BOUNDARY.txt", "LICENSE", "COPYRIGHT_NOTICE.txt", "THIRD_PARTY_NOTICES.txt"})
checks["manifest:sha256_format"] = all(re.fullmatch(r"[0-9a-f]{64}", d or "") for d in manifest.values())
checks["manifest:professional_names"] = all(Path(name).name == name and ".." not in name for name in REQUIRED)
for name, digest in manifest.items():
    path = ROOT / name
    checks[f"sha256:{name}"] = path.is_file() and sha256(path) == digest

s = load(HTML)
readme = load(ROOT / "README.md")
boundary = load(ROOT / "SCIENTIFIC_BOUNDARY.txt")
license_text = load(ROOT / "LICENSE")
copyright_text = load(ROOT / "COPYRIGHT_NOTICE.txt")
third_party = load(ROOT / "THIRD_PARTY_NOTICES.txt")
all_text = "\n".join([s, readme, boundary, license_text, copyright_text, third_party])
ids_list = re.findall(r'\bid=["\']([^"\']+)["\']', s)
ids = set(ids_list)
refs = set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', s))
small_sizes = [float(x) for x in re.findall(r"font-size:([0-9.]+)px", s) if float(x) < 10]


def add_tokens(prefix, source, tokens, ci=False):
    src = source.lower() if ci else source
    for i, token in enumerate(tokens, 1):
        t = token.lower() if ci else token
        checks[f"{prefix}:{i:03d}"] = t in src


add_tokens("identity", s, [
    "<title>Solar System Time Journey (SSTJ) v1.5.0</title>",
    '<span class="version">v1.5.0</span>',
    "SOLAR SYSTEM TIME JOURNEY",
    'class="brand-short">SSTJ</span>',
    'application:"Solar System Time Journey"',
    'application_abbreviation:"SSTJ"',
    'schema:"solar_system_time_journey_v1_5_0"',
    'scope:"observer_place_time_record"',
    "Solar_System_Time_Journey_Record_",
    "Journey record integrity",
    "Breadcrumb chain root",
    "Measurement quality",
    "Route directness",
    "Segment qualification",
    "Browser capabilities",
    "Solar Splits",
    "Recent Journeys",
    "Journey Signal",
])
checks["identity:html_filename"] = HTML.name == "Solar_System_Time_Journey_v1_5_0.html"
checks["identity:no_certificate_language"] = "journey certificate" not in all_text.lower()

checks["dom:no_duplicate_ids"] = len(ids_list) == len(ids)
checks["dom:all_getElementById_refs_exist"] = refs.issubset(ids)
required_ids = [
    "space","journeyBtn","journeyShell","journeyTitle","journeyStatus","startJourneyBtn","demoJourneyBtn","pauseJourneyBtn","endJourneyBtn","exportJourneyBtn","clearJourneyBtn",
    "landingPreference","landingPreferenceHint","distanceUnitPreference","distanceUnitPreferenceHint","goalType","goalValue","goalUnit","goalHint","strideInput","journeyGpsNote","routeCanvas","motionCanvas",
    "jGround","jSteps","jElapsed","jActiveTime","jPausedTime","jMoving","jStopped","jSpeed","jAvgSpeed","jMaxSpeed","jPace","jElevGain","jElevLoss","jFromStart","jRotation","jOrbit","jSamples",
    "jSignal","jContinuity","jGoalProgress","jLatestSplit","jLat","jLon","jAlt","jAcc","jActivity","jRetention","jDistanceQualified","jDistanceRejected","jQuality","jAccuracySummary","jDirectness","jSegments","jTimestampQuality","jCapabilities",
    "jGoalState","jSplitCount","jContinuityEvents","jStartUTC","jCurrentUTC","jStartFP","jCurrentFP","jIntegrityMode","jEndUTC","jEndFP","jRecordDigest","jChainRoot","solarSplitList","recentJourneyList","clearRecentJourneysBtn",
    "helpShell","helpTitle","helpBody","dateInput","phaseList","fingerprint"
]
for rid in required_ids:
    checks[f"dom:id:{rid}"] = rid in ids

security = {
    "csp:meta": 'http-equiv="Content-Security-Policy"' in s,
    "csp:default_none": "default-src 'none'" in s,
    "csp:connect_none": "connect-src 'none'" in s,
    "csp:object_none": "object-src 'none'" in s,
    "csp:base_none": "base-uri 'none'" in s,
    "csp:form_none": "form-action 'none'" in s,
    "csp:inline_script": "script-src 'unsafe-inline'" in s,
    "csp:inline_style": "style-src 'unsafe-inline'" in s,
    "privacy:no_referrer": '<meta name="referrer" content="no-referrer">' in s,
    "network:no_fetch": "fetch(" not in s,
    "network:no_xhr": "XMLHttpRequest" not in s,
    "network:no_websocket": "WebSocket" not in s,
    "network:no_eventsource": "EventSource" not in s,
    "network:no_sendbeacon": "sendBeacon" not in s,
    "network:no_external_script": not bool(re.search(r"<script[^>]+src=", s, re.I)),
    "network:no_external_stylesheet": not bool(re.search(r'<link[^>]+rel=["\']stylesheet', s, re.I)),
    "network:no_external_http_urls": not bool(re.search(r"https?://", s, re.I)),
    "security:no_eval": "eval(" not in s,
    "security:no_function_constructor": "new Function" not in s and "Function(" not in s,
    "security:no_debugger": "debugger" not in s,
    "security:no_map_tiles": "openstreetmap" not in s.lower() and "maps.googleapis" not in s.lower(),
}
checks.update(security)

add_tokens("planet", s, [
    "ELEMENT_WINDOW_MIN_MS","ELEMENT_WINDOW_MAX_MS","epochInElementWindow","clampElementEpoch","planetarySnapshot","heliocentric_longitudes_deg",
    "display_fingerprint_non_cryptographic","earthOrbitSpeedKmS","helioLon","Mercury","Venus","Earth","Mars","Jupiter","Saturn","Uranus","Neptune",
    "1800-01-01T00:00:00","2050-12-31T23:59:59","Heliocentric ecliptic","J2000 elements","low-precision"
])

add_tokens("geodesy", s, [
    "WGS84_A_KM=6378.137","WGS84_F=1/298.257223563","WGS84_B_KM=WGS84_A_KM*(1-WGS84_F)","MEAN_EARTH_RADIUS_KM=6371.0088",
    "function geodesicDistanceKm(a,b)",'solver:"WGS84_VINCENTY"','solver:"MEAN_RADIUS_HAVERSINE_FALLBACK"',"if(iter>=100)",
    "function destinationPoint(lat,lon,bearing,distanceKm)","function haversineKm(a,b)","function distanceFromStartKm()",
    'ground_distance_model:"WGS84_VINCENTY_INVERSE_WITH_MEAN_RADIUS_HAVERSINE_FALLBACK"',"ground_wgs84_semi_major_axis_km:WGS84_A_KM","ground_wgs84_flattening:WGS84_F",
    "geodesic_fallback_radius_km:MEAN_EARTH_RADIUS_KM","geodesicFallbackCount","rawCoordinateGroundKm","raw_coordinate_path_km","ground_path_km","route_directness_ratio","function routeDirectness()"
])

add_tokens("quality", s, [
    "DISTANCE_ACCURACY_MAX_M=35","POSITION_STALE_MAX_MS=90000","MOTION_SIGNAL_MIN=0.5","function distanceFixQualified(sample)","function emptyAccuracyHistogram()",
    "function addAccuracyObservation(value)","function accuracyQuantileApprox(q)","function measurementQualitySummary()",'grade:"SYNTHETIC"','grade="INSUFFICIENT"','grade="HIGH"','grade="MODERATE"','grade="LIMITED"',
    "reportedAccuracySamples","accuracyHistogram","distanceRejectedAccuracySamples","distanceRejectedTemporalSamples","staleFixCount","nonmonotonicTimestampCount","providerTimestampFallbackCount","segmentAcceptedCount","segmentRejectedNoiseCount","segmentRejectedSpeedCount","segmentRejectedTemporalCount","segmentRejectedShortIntervalCount","segmentRejectedUnqualifiedPairCount",
    "browser_reported_horizontal_accuracy_median_m_approx","browser_reported_horizontal_accuracy_p95_m_approx","rejected_fix_fraction","geodesic_fallback_count","segments_accepted","segments_rejected"
])

add_tokens("segment", s, [
    "FIRST_FIX","ACCEPTED","REJECTED_UNQUALIFIED_FIX_PAIR","REJECTED_STALE_TIMESTAMP","REJECTED_NONPOSITIVE_DT","REJECTED_INTERVAL_TOO_SHORT","REJECTED_TOO_SMALL_FOR_POSITIONAL_NOISE","REJECTED_IMPLAUSIBLE_SPEED",
    "pairAccuracy=Math.hypot","noiseThresholdM=sample.synthetic?0:Math.max(2,Math.min(25,pairAccuracy*MOTION_SIGNAL_MIN))","motionSignal=pairAccuracy>0?segKm*1000/pairAccuracy:null",
    "counted_ground_segment","distance_rejection_reason","segment_state","raw_coordinate_segment_km","qualified_ground_segment_km","positional_noise_threshold_m","motion_signal_ratio"
])

add_tokens("timestamp", s, [
    "provider_timestamp_ms","provider_timestamp_supplied","callback_wall_ms","callback_monotonic_ms","position_age_ms","temporal_qualified","providerTimestampSupplied","callbackWallMs","callbackMonotonicMs","performance.now()",
    "sample.position_age_ms>POSITION_STALE_MAX_MS","journey.nonmonotonicTimestampCount++","dt=(sample.ms-prev.ms)/1000","if(!(dt>0))","if(dt>90)journey.unclassifiedSeconds+=dt"
])

add_tokens("provenance", s, [
    "function exportBreadcrumb(sample)","observed:{","derived:{","latitude_deg:sample.lat","longitude_deg:sample.lon","altitude_m:sample.alt","horizontal_accuracy_m:sample.accuracy_m","altitude_accuracy_m:sample.altitude_accuracy_m",
    "reported_speed_mps:sample.reported_speed_mps","reported_heading_deg:sample.reported_heading_deg","provider_timestamp_ms:sample.provider_timestamp_ms","callback_wall_ms:sample.callback_wall_ms","callback_monotonic_ms:sample.callback_monotonic_ms",
    "position_age_ms:sample.position_age_ms","distance_qualified:sample.distance_qualified","distance_rejection_reason:sample.distance_rejection_reason","segment_state:sample.segment_state","raw_coordinate_segment_km:sample.raw_coordinate_segment_km","qualified_ground_segment_km:sample.ground_segment_km",
    "resolved_speed_mps:sample.speed_mps","resolved_heading_deg:sample.heading_deg","planetary_display_fingerprint_non_cryptographic","browser_capability_observation","reported_speed_fraction","reported_heading_fraction","reported_altitude_fraction","reported_altitude_accuracy_fraction"
])

add_tokens("integrity", s, [
    "function sha256Bytes(bytes)","function sha256Text(text)",'crypto.subtle.digest("SHA-256",bytes)',"async function journeyDigest()","record_sha256","recordDigest:null","journey.recordDigest=digest","!journey.recordDigest",
    "function canonicalBreadcrumbForChain(sample)","function verifyRetainedBreadcrumbChain()","breadcrumb_previous_sha256","breadcrumb_chain_sha256","breadcrumbChainGenesis","breadcrumbChainHash","SHA256_APPEND_ONLY_HASH_CHAIN",'algorithm:"SHA-256"',
    "genesis_sha256","retained_start_previous_sha256","final_root_sha256","tamper-evident append-only breadcrumb ordering and content","not proof of physical presence or location authenticity","breadcrumb_chain_scope","record_digest_scope"
])

add_tokens("retention", s, [
    "MAX_BREADCRUMBS=5000","function orderedJourneySamples()","function appendJourneySample(sample)","sampleHead","droppedGroundKm","droppedSamples","retainedGroundKm()","FIXED_CAP_CIRCULAR_BUFFER","breadcrumb_storage",
    "reconciled_ground_path_km","reconciliation_error_km_unrounded","comparison within serialization rounding; not exact bit equality","retained_breadcrumbs","total_breadcrumbs"
])

add_tokens("fitness", s, [
    "STRIDE_MIN=0.30","STRIDE_MAX=2.50","strideM:.78","strideM:1.05","function effectiveStrideM(name)","function estimatedSteps()","step_estimate_stride_m","step_estimate_stride_source","step_estimate_stride_default_m",
    "movingSeconds","stoppedSeconds","unclassifiedSeconds","average_moving_speed_kmh_approx","average_pace_seconds_per_km_approx","elevationGainM","elevationLossM","elevationQualifiedIntervals","Math.max(2.5,Math.hypot","ALTITUDE_ACCURACY_GATED",
    "BOUNDED_REPORTED_SPEED_ELSE_SEGMENT_DERIVED","ACCEPTED_SEGMENT_DERIVED","earthRotationSpeedKmS","earthOrbitSpeedKmS"
])

add_tokens("landing", s, [
    'LANDING_STORAGE_KEY="sstj_landing_preference_v1"',"function safeLocalGet(key)","function safeLocalSet(key,value)","function normalizeLandingPreference(value)","function readLandingPreference()","function saveLandingPreference(value)",
    'matchMedia("(max-width:760px)").matches?"journey":"planet"',"function effectiveLandingScreen()","function applyLandingPreference()",'id="landingPreference"','value="automatic"','value="planet"','value="journey"',
    "Automatic: Planet View on desktop, Journey View on mobile."
])

add_tokens("units", s, [
    "KM_PER_MI=1.609344","MI_PER_KM=1/KM_PER_MI",'UNIT_STORAGE_KEY="sstj_distance_unit_v1"',"function normalizeDistanceUnit(value)","function readDistanceUnit()","function currentDistanceUnit()","function saveDistanceUnit(value)",
    "function distanceDisplayValue(km,unit=currentDistanceUnit())","function distanceCanonicalKm(value,unit=readDistanceUnit())","function speedDisplayValue(kmh,unit=currentDistanceUnit())","function paceSecondsForDisplay(secondsPerKm,unit=currentDistanceUnit())",
    "function splitDisplayDistanceForActivity(name)","function splitDistanceForActivity(name,unit=readDistanceUnit())","function updateDistanceUnitUI()",'id="distanceUnitPreference"','value="km"','value="mi"',
    'distanceUnit:"km"','goalDisplayValue:null','goalDisplayUnit:null','splitDisplayDistance:1','splitDisplayUnit:"km"','display_preferences:{distance_unit_at_start:journey.distanceUnit,canonical_distance_unit:"km",canonical_length_unit:"m"}',
    'canonical_value_km:journey.goalType==="distance"?journey.goalValue:null',"declared_distance_interval:journey.splitDisplayDistance","declared_distance_unit:journey.splitDisplayUnit","distance_unit_at_start:journey.distanceUnit",
    'distance_unit_preference:"optional browser-local kilometre/mile display preference; canonical geometry and record quantities remain metric"',"1 km or 1 mile","5 km or 5 miles"
])
checks["units:exact_mile_conversion"] = "1.609344" in s and "KM_PER_MI=1.609344" in s
checks["units:no_dynamic_browser_unit_in_record"] = "current_browser_distance_unit" not in s

add_tokens("pause", s, [
    "function pausedSeconds(","function activeDurationSeconds(","manualPausedMs","pauseCount","pauseStartedMs","function pauseJourney()","function resumeJourney()","function togglePauseJourney()","MANUAL_PAUSE","MANUAL_RESUME",
    "journey.lastSample=null","journey.elevationAnchorAlt=null","journey.elevationAnchorAccuracy=null","releaseJourneyWakeLock()","startGpsWatch()","startDemoWalk()",'pause.textContent=journey.paused?"RESUME":"PAUSE"',
    "active_seconds","manual_paused_seconds","manual_pause_count",'pause:"manual Pause stops ground acquisition and prevents cross-pause segment construction; it does not stop physical time, Earth rotation, Earth orbit, or the planetary clock"'
])

add_tokens("goal", s, [
    "goalDraftValues={distanceKm:5,distanceMi:5,time:30}","function refreshGoalControl()","function readGoalConfig()",'valueEl.min="0.1"','valueEl.max="1000"','valueEl.min="1"','valueEl.max="1440"',
    "goalType","goalValue","goalAchievedMs","goalAchievedGroundKm","function goalProgressData(","function markGoalAchieved(","function maybeMarkTimeGoal(","function maybeMarkDistanceGoal(","GOAL_ACHIEVED",
    "goal:{","type:journey.goalType","canonical_value_km:journey.goalType===\"distance\"?journey.goalValue:null","status:journey.goalType===\"none\"?\"NO_GOAL\":journey.goalAchievedMs!==null?\"ACHIEVED\":\"INCOMPLETE\"","active Journey time with manual pauses excluded"
])

add_tokens("splits", s, [
    "MAX_SOLAR_SPLITS=2000","splitKm:1","splitKm:5","function splitDisplayDistanceForActivity(name)","function splitDistanceForActivity(name,unit=readDistanceUnit())","function captureSolarSplits(","split_number","cumulative_ground_km","split_distance_km","display_unit_at_start","cumulative_ground_display","split_distance_display","cumulative_active_seconds","split_active_seconds",
    "split_pace_seconds_per_km_approx","split_average_speed_kmh_approx","planetary_state","associated_breadcrumb_chain_sha256",'model:"distance milestone interpolated within an accepted WGS84 segment"',"SOLAR_SPLIT","solar_splits:{","function renderSolarSplits()"
])

add_tokens("signal", s, [
    "function journeySignal()",'return"PAUSED"','return"SYNTHETIC"','return"SEALED"','return"EXCELLENT"','return"GOOD"','return"LIMITED"','return"WAITING"',"accuracy_m<=8","accuracy_m<=15","accuracy_m<=DISTANCE_ACCURACY_MAX_M","function journeySignalClass(signal)","jSignal"
])

add_tokens("continuity", s, [
    "MAX_CONTINUITY_EVENTS=500","GEOLOCATION_GAP_MS=15000","function recordContinuityEvent(","function continuityInterruptionCount()","function continuityState()","visibilityHiddenCount","geolocationGapCount","wakeLockLossCount","wakeLockReacquireCount",
    "WAKE_LOCK_REACQUIRED","WAKE_LOCK_LOST","PAGE_HIDDEN","PAGE_VISIBLE","GEOLOCATION_GAP","continuity:{","interruption_event_count","visibility_hidden_count","geolocation_gap_count","wake_lock_loss_count","wake_lock_reacquire_count","geolocation_gap_threshold_ms:GEOLOCATION_GAP_MS"
])

add_tokens("recent", s, [
    "RECENT_JOURNEY_LIMIT=20",'RECENT_STORAGE_KEY="sstj_recent_journeys_v1"',"function loadRecentJourneys()","function storeRecentJourneySummary()","function renderRecentJourneys()","function clearRecentJourneys()","recentSummaryStored",
    "distance_unit_at_start:journey.distanceUnit","ground_path_km:Number(journey.groundKm.toFixed(3))","active_seconds:Number(activeDurationSeconds(journey.endMs).toFixed(1))","manual_paused_seconds:Number(pausedSeconds(journey.endMs).toFixed(1))","measurement_quality:measurementQualitySummary().grade",
    "goal_achieved:journey.goalAchievedMs!==null","solar_split_count:journey.splits.length","record_sha256:journey.recordDigest","local_storage_policy:{","route coordinates and breadcrumb arrays are not stored in Recent Journeys","full Journey record is retained only when the user explicitly exports JSON"
])
checks["recent:no_coordinates_in_summary_object"] = "latitude_deg:" not in s[s.find("function storeRecentJourneySummary"):s.find("function renderRecentJourneys")]
checks["recent:no_breadcrumbs_in_summary_object"] = "breadcrumbs" not in s[s.find("function storeRecentJourneySummary"):s.find("function renderRecentJourneys")].lower()

add_tokens("selftest", s, [
    "async function runSSTJSelfTest()","Schema identity","Planetary lower guard","Planetary upper guard","WGS84 equatorial degree","WGS84 meridional degree","WGS84 direct-inverse closure","SHA-256 reference","Accuracy gate rejects poor fix","Poor fix adds no distance","No bridge across poor fix","Segment acceptance count","Raw coordinate path retained","Route directness unavailable across gap","Custom stride frozen","Breadcrumb hash chain root","Breadcrumb hash chain verification","Observed-derived separation","Measurement quality block","Digest reproducible","Accuracy-relative jitter rejection","Short interval rejection","Nonmonotonic timestamp rejection","Landing preference normalization","Distance unit normalization","Kilometre-mile conversion","Activity Solar Split defaults","Mile Solar Split defaults","Active duration excludes manual pause","Journey Signal excellent gate","Journey Signal waits on unqualified fix","Solar Split threshold capture","Solar Split chain binding","Distance goal interpolated achievement","Goal and split record blocks","Unit metadata record block","Observed callback wall provenance","Pause-style anchor reset prevents bridge","Continuity event capture","Continuity record block","Ride steps unavailable","Reset split follows selected activity","Circular retention cap","Circular chronology","Circular reconciliation","SSTJ SELF-TEST:"
])

add_tokens("accessibility", s, [
    '@media(prefers-reduced-motion:reduce)','id="journeyShell" aria-hidden="true" inert','id="helpShell" aria-hidden="true" inert',"function focusOutsideBeforeHide(shell,target)","function closeModalAfterFocus(shell,target,finish,attempt=0)","function trapModalFocus(e,shell)",'aria-live="polite"','role="dialog" aria-modal="true"'
])
checks["accessibility:no_authored_sub10_px"] = len(small_sizes) == 0
checks["accessibility:scientific_copy_subordinate"] = ".clock-boundary-lead{font-size:15px" in s and "@media(max-width:760px)" in s

add_tokens("readme", readme, [
    "SOLAR SYSTEM TIME JOURNEY (SSTJ) v1.5.0","observer motion != change to planetary clock state","Automatic: Planet View on desktop, Journey View on mobile","Distance-unit preference","1 mi = 1.609344 km","canonical_distance_unit = km","distance_goal_km = distance_goal_display * 1.609344","active_time = wall_elapsed_time - manual_paused_time","manual_pause != pause of planetary state","Solar Splits","f = (D_target - D_before) / segment_distance","Journey Signal","callback_gap_ms > 15000","Recent Journeys","route coordinates","WGS84 ellipsoidal ground-distance calculation","WGS84_A_KM = 6378.137","WGS84_F = 1 / 298.257223563","MEAN_EARTH_RADIUS_KM = 6371.0088","reported_horizontal_accuracy_m <= 35","position_age_ms <= 90000","motion_signal_min_ratio = 0.5","raw_coordinate_path_km","ground_path_km","route_directness_ratio","Measurement-quality state","Observed and derived data","Browser capability variability","H_0 = SHA256(journey_chain_header)","H_n = SHA256(H_(n-1) || canonical_breadcrumb_n)","MAX_BREADCRUMBS = 5000","record SHA-256 != proof of presence","breadcrumb SHA-256 chain != proof of presence","await runSSTJSelfTest()","contains 50 checks","real-device field testing","secure top-level HTTPS browser context"
], ci=True)

add_tokens("boundary", boundary, [
    "SOLAR SYSTEM TIME JOURNEY (SSTJ) v1.5.0 - SCIENTIFIC BOUNDARY","observer motion -> changed planetary clock","Distance-unit preference","1 mi = 1.609344 km","canonical geometry and scientific record quantities remain metric","Manual Pause does not stop physical time","active_time = wall_elapsed_time - manual_paused_time","distance goals are declared in the unit frozen at Journey start","distance_goal_km = distance_goal_mi * 1.609344","Solar Splits","f = (D_target - D_before) / segment_distance","Journey Signal","callback_gap_ms > 15000","Recent Journey summaries exclude route coordinates and breadcrumb arrays","The browser API does not guarantee","WGS84 ellipsoidal Vincenty inverse","reported_horizontal_accuracy_m <= 35","position_age_ms <= 90000","motion_signal_min_ratio = 0.5","REJECTED_TOO_SMALL_FOR_POSITIONAL_NOISE","REJECTED_IMPLAUSIBLE_SPEED","REJECTED_NONPOSITIVE_DT","REJECTED_INTERVAL_TOO_SHORT","raw_coordinate_path_km","route_directness_ratio","does not convert per-fix browser accuracy into a cumulative route-distance confidence interval","Observed values can include","Derived values can include","estimated_steps =","elevation_threshold_m =","H_0 = SHA256(journey_chain_header)","record SHA-256 != proof of presence","a navigation-certified geodesy product","a proof-of-presence system","local file is not treated as the primary live-geolocation deployment environment"
], ci=True)

rights = {
    "rights:license_identity": "Solar System Time Journey (SSTJ)" in license_text,
    "rights:apache": "Apache License, Version 2.0" in license_text,
    "rights:cc_by_nc": "CC BY-NC 4.0" in license_text,
    "rights:copyright": "Copyright © 2026 Shunyaya Framework contributors." in copyright_text,
    "rights:third_party_jpl": "NASA/JPL" in third_party,
    "rights:third_party_wgs84": "WGS84" in third_party,
    "rights:third_party_web_storage": "Web Storage API" in third_party,
    "rights:no_bundled_geodesic_library": "No third-party geodesic source code or runtime library is bundled." in third_party,
    "rights:no_runtime_assets": "does not bundle third-party JavaScript" in third_party,
    "rights:no_rights_override": "No rights override" in third_party,
}
checks.update(rights)

checks["hygiene:version_set"] = set(re.findall(r"v\d+\.\d+\.\d+", all_text)) <= {"v1.5.0"}
checks["hygiene:html_version_set"] = set(re.findall(r"v\d+\.\d+\.\d+", s)) <= {"v1.5.0"}
checks["hygiene:professional_file_names"] = all(Path(name).name == name and ".." not in name for name in REQUIRED)

m_a = re.search(r"\bWGS84_A_KM\s*=\s*([0-9.]+)", s)
m_r = re.search(r"\bMEAN_EARTH_RADIUS_KM\s*=\s*([0-9.]+)", s)
m_f = re.search(r"\bWGS84_F\s*=\s*1/([0-9.]+)", s)
a = float(m_a.group(1)) if m_a else None
mean_r = float(m_r.group(1)) if m_r else None
f = 1 / float(m_f.group(1)) if m_f else None
checks["numeric:wgs84_a_extracted"] = a is not None and abs(a - 6378.137) < 1e-12
checks["numeric:mean_radius_extracted"] = mean_r is not None and abs(mean_r - 6371.0088) < 1e-12
checks["numeric:wgs84_f_extracted"] = f is not None and abs(f - 1 / 298.257223563) < 1e-16
if a is not None and f is not None:
    eq = vincenty_km(0, 0, 0, 1, a, f)
    mer = vincenty_km(0, 0, 1, 0, a, f)
    checks["numeric:wgs84_equatorial_degree"] = eq is not None and abs(eq - 111.319490793) < 1e-6
    checks["numeric:wgs84_meridional_degree"] = mer is not None and abs(mer - 110.574388558) < 1e-6
else:
    checks["numeric:wgs84_equatorial_degree"] = False
    checks["numeric:wgs84_meridional_degree"] = False

passed = sum(bool(v) for v in checks.values())
total = len(checks)
print("Solar System Time Journey (SSTJ) v1.5.0 verifier")
for name, value in checks.items():
    print(f'{name}:{"PASS" if value else "FAIL"}')
print(f'checks:{passed}/{total} {"PASS" if passed == total else "FAIL"}')
sys.exit(0 if passed == total else 1)
