#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Solar System Clock Structure Verifier v1.0.4.

Checks package/UI structure and offline properties only. It is not an
astronomical accuracy validator.
"""
from pathlib import Path
import re
FILE=Path(__file__).with_name("Solar_System_Clock_v1_0_4.html")
s=FILE.read_text(encoding="utf-8")
checks={
"doctype":s.lstrip().lower().startswith("<!doctype html>"),
"single_file":True,
"no_fetch":"fetch(" not in s,
"no_xhr":"XMLHttpRequest" not in s,
"no_websocket":"WebSocket" not in s,
"no_external_script":not bool(re.search(r'<script[^>]+src=',s,re.I)),
"no_external_stylesheet":not bool(re.search(r'<link[^>]+rel=["\']stylesheet',s,re.I)),
"title":"<title>Solar System Clock v1.0.4</title>" in s,
"center_instrument":'class="center"' in s and "border:3px solid rgba(241,193,93,.92)" in s,
"live_longitudes":'id="phaseList"' in s and "helioLon(p.name,jd)" in s,
"longitude_rate":"°/d" in s,
"motion_trails":"showTrails" in s,
"compact_laptop":"@media(max-height:680px)" in s,
"viewport_fit":"height:calc(100dvh - 44px)" in s,
"phone_breakpoint":"@media(max-width:760px)" in s,
"phone_vertical_stack":"display:flex;flex-direction:column" in s and ".center{\n    order:1;width:100%" in s,
"phone_natural_height":"height:auto;min-height:calc(100dvh - 44px)" in s,
"phone_center_full_width":"order:1;width:100%;height:clamp(340px,102vw,430px)" in s,
"phone_controls_second":"order:2;width:100%;display:grid" in s,
"phone_left_panel_third":".left{order:3;width:100%;display:flex" in s,
"phone_right_panel_fourth":".right{order:4;width:100%;display:flex" in s,
"phone_speed_scroll":"overflow-x:auto;overflow-y:hidden" in s and "-webkit-overflow-scrolling:touch" in s,
"phone_longitudes_readable":".longitudes{min-height:430px}" in s and "#phaseList{min-height:360px}" in s,
"small_phone_breakpoint":"@media(max-width:380px)" in s,
"powered_footer":"Powered by Shunyaya Framework" in s,
"seven_decimal_live_longitude":"toFixed(7)" in s,
"live_delta_indicator":'class="delta"' in s and "deltaReferenceLongitudes" in s,
"delta_initialization_order":s.find("let deltaReferenceJD=") < s.find("for(const p of PLANETS)deltaReferenceLongitudes[p.name]"),
"default_30d_per_second":"speed=2592000" in s and 'data-speed="2592000">30d/s' in s,
"now_resets_1x":'b.dataset.speed==="1"' in s and "speed=1" in s,
"low_precision_label":"LOW-PRECISION ORBITAL MODEL" in s and '+" • LOW-PRECISION ORBITAL MODEL"' in s,
"non_cryptographic_fingerprint_label":"Display fingerprint (non-cryptographic)" in s,
"demo_accuracy_boundary":"not precision ephemerides" in s.lower(),
}
p=sum(checks.values())
print("Solar System Clock Structure Verifier v1.0.4")
print("scope:UI/offline/structure only; not astronomical validation")
for k,v in checks.items():print(f"{k}:{'PASS' if v else 'FAIL'}")
print(f"checks:{p}/{len(checks)} {'PASS' if p==len(checks) else 'FAIL'}")
raise SystemExit(0 if p==len(checks) else 1)
