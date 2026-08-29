SOLAR SYSTEM CLOCK v1.0.4
=========================

Standalone interactive reference/demo for Solar System Time.

Default
-------
The clock opens at the current epoch and advances at 30 days/second so that
planetary motion is immediately visible. The accelerated display is labelled
SIMULATED EPOCH. Press NOW to return to current UTC at 1x.

Accuracy label
--------------
The displayed positions use a low-precision approximate orbital model. The
clock is a visualization/reference application, not a precision ephemeris and
not an astronomical validation tool.

The displayed fingerprint is explicitly labelled non-cryptographic. It is a
compact visual state identifier, not an integrity or security primitive.

Files
-----
Solar_System_Clock_v1_0_4.html
Solar_System_Clock_v1_0_4_Verifier.py

Verify structure/offline properties
-----------------------------------
python -B Solar_System_Clock_v1_0_4_Verifier.py

The verifier checks HTML structure, offline/self-contained properties, UI
features, default 30d/s behavior, NOW->1x behavior, and known regression guards.
It does not validate astronomical accuracy or the observational result.

Mobile layout:
- At phone widths (<=760 px), the instrument, controls, epoch/reference cards, and live-longitude panel stack vertically.
- The layout is designed to avoid horizontal page scrolling; speed controls may scroll within their own control strip when needed.

