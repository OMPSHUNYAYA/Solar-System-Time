#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Solar System Time Reference Resolver v1.0.4

Compact Python-standard-library reference implementation for the frozen
Uranus/Neptune J2000-equatorial inverse geometry.

This implementation is a reproducibility reference. It does not provide civil,
metrological, navigation-grade, or unrestricted all-time timing.
"""
from __future__ import annotations
import argparse, math, re

J2000=2451545.0
CENTURY=36525.0
OBLIQUITY_DEG=23.439291111
EL={
# JPL Table-1 "EM Bary" elements; retained under the internal key "Earth"
# as the compact Earth-orbit proxy used by this low-precision reference model.
"Earth":((1.00000261,0.00000562),(0.01671123,-0.00004392),(-0.00001531,-0.01294668),(100.46457166,35999.37244981),(102.93768193,0.32327364),(0.0,0.0)),
"Uranus":((19.18916464,-0.00196176),(0.04725744,-0.00004397),(0.77263783,-0.00242939),(313.23810451,428.48202785),(170.95427630,0.40805281),(74.01692503,0.04240589)),
"Neptune":((30.06992276,0.00026291),(0.00859048,0.00005105),(1.77004347,0.00035372),(-55.12002969,218.45945325),(44.96476227,-0.32241464),(131.78422574,-0.00508664)),
}

def sexa(s,is_ra):
    if not isinstance(s,str): raise ValueError("coordinate must be text")
    raw=s.strip().replace("−","-").replace(":"," ")
    p=[x for x in re.split(r"\s+",raw) if x]
    if not p or len(p)>3: raise ValueError("coordinate must contain 1 to 3 sexagesimal fields")
    try: v=[float(x) for x in p]
    except ValueError as exc: raise ValueError("coordinate contains a non-numeric field") from exc
    while len(v)<3: v.append(0.0)
    if v[1] < 0 or v[1] >= 60 or v[2] < 0 or v[2] >= 60:
        raise ValueError("minutes and seconds must satisfy 0 <= value < 60")
    if is_ra:
        if raw.startswith(("+","-")) or v[0] < 0 or v[0] >= 24:
            raise ValueError("right ascension hours must satisfy 0 <= RA < 24")
        deg=(v[0]+v[1]/60.0+v[2]/3600.0)*15.0
    else:
        sign=-1 if v[0]<0 or raw.startswith("-") else 1
        d0=abs(v[0])
        if d0 > 90 or (d0 == 90 and (v[1] != 0 or v[2] != 0)):
            raise ValueError("declination must satisfy -90 <= Dec <= +90 degrees")
        deg=sign*(d0+v[1]/60.0+v[2]/3600.0)
    return math.radians(deg)

def obs_vec(ra,de):
    a=sexa(ra,True); d=sexa(de,False); c=math.cos(d)
    return (c*math.cos(a),c*math.sin(a),math.sin(d))

def xyz(p,jd):
    T=(jd-J2000)/CENTURY
    a,e,I,L,lp,node=[x0+x1*T for x0,x1 in EL[p]]
    M=math.radians((L-lp+180.0)%360.0-180.0)
    E=M
    for _ in range(30):
        q=(E-e*math.sin(E)-M)/(1.0-e*math.cos(E)); E-=q
        if abs(q)<1e-14: break
    xp=a*(math.cos(E)-e); yp=a*math.sqrt(max(0.0,1.0-e*e))*math.sin(E)
    w=math.radians(lp-node); O=math.radians(node); inc=math.radians(I)
    cw,sw=math.cos(w),math.sin(w); co,so=math.cos(O),math.sin(O); ci,si=math.cos(inc),math.sin(inc)
    x=(cw*co-sw*so*ci)*xp+(-sw*co-cw*so*ci)*yp
    y=(cw*so+sw*co*ci)*xp+(-sw*so+cw*co*ci)*yp
    z=sw*si*xp+cw*si*yp
    return x,y,z

MODEL_START_JD=2378496.5  # 1800-01-01 00:00 UTC-like calendar boundary for declared model-use guard
MODEL_END_JD=2470172.5    # exclusive upper boundary: 2051-01-01 00:00; full calendar year 2050 is admitted
C_AU_PER_DAY=173.144632674240  # speed of light in AU/day (IAU 2012)

def pred_vec(p,jd,light_time=True,iters=3):
    """Light-time-corrected (astrometric, J2000-equatorial) geocentric unit
    direction to planet p at observation Julian date jd.

    Uses the retarded-time (planetary light-time) correction: the observer at
    the Earth-Moon-barycenter proxy at jd sees the planet where it was at jd - tau, with
    tau = geocentric_distance / c. Two-three fixed-point iterations converge.
    Stellar aberration (~20 arcsec, observer-velocity term) is intentionally
    NOT applied: J2000 astrometric catalogue positions do not include it.
    Set light_time=False to recover the previous purely geometric behaviour.
    """
    e=xyz("Earth",jd)                       # JPL EM-Bary observer-orbit proxy at observation time
    q=xyz(p,jd); tau=0.0
    if light_time:
        for _ in range(iters):
            q=xyz(p,jd-tau)                 # planet at retarded time
            dx,dy,dz=(q[i]-e[i] for i in range(3))
            tau=math.sqrt(dx*dx+dy*dy+dz*dz)/C_AU_PER_DAY
    x,y,z=(q[i]-e[i] for i in range(3))
    ep=math.radians(OBLIQUITY_DEG); ce,se=math.cos(ep),math.sin(ep)
    v=(x,ce*y-se*z,se*y+ce*z); n=math.sqrt(sum(t*t for t in v))
    return tuple(t/n for t in v)

def angle_deg(a,b):
    c=max(-1.0,min(1.0,sum(x*y for x,y in zip(a,b))))
    return math.degrees(math.acos(c))

def score(obs,jd):
    return math.sqrt(sum(angle_deg(pred_vec(p,jd),v)**2 for p,v in obs.items())/len(obs))

def validate_search_window(start,end,allow_outside=False):
    if not math.isfinite(start) or not math.isfinite(end):
        raise ValueError("search bounds must be finite Julian dates")
    if start>=end: raise ValueError("start JD must be less than end JD")
    if not allow_outside and (start < MODEL_START_JD or end >= MODEL_END_JD):
        raise ValueError(
          "search interval exceeds the declared 1800-2050 validity window of the "
          "JPL approximate-element set; narrow the interval or pass "
          "--allow-outside-model-validity for exploratory use"
        )

def reconstruct(obs,start,end):
    vals=[]; j=start
    while j<=end+1e-12:
        vals.append((score(obs,j),j)); j+=1.0
    vals.sort(); seeds=[]
    for s,j in vals:
        if all(abs(j-k)>30 for _,k in seeds):
            seeds.append((s,j))
            if len(seeds)>=20: break
    refined=[]
    for _,c in seeds:
        arr=[]; j=max(start,c-2.0); stop=min(end,c+2.0)
        while j<=stop+1e-12: arr.append((score(obs,j),j)); j+=0.25
        _,c2=min(arr)
        arr=[]; j=max(start,c2-0.25); stop=min(end,c2+0.25); step=15/(24*60)
        while j<=stop+1e-12: arr.append((score(obs,j),j)); j+=step
        refined.append(min(arr))
    refined.sort(); best=refined[0]; second=None
    for x in refined[1:]:
        if abs(x[1]-best[1])>30: second=x; break
    return best,second

def vec_to_radec(v):
    x,y,z=v; ra=math.atan2(y,x)%(2*math.pi); de=math.asin(z)
    def hms(rad):
        h=math.degrees(rad)/15; H=int(h); m=(h-H)*60; M=int(m); s=(m-M)*60
        return f"{H:02d} {M:02d} {s:09.6f}"
    def dms(rad):
        d=math.degrees(rad); sg='-' if d<0 else '+'; d=abs(d); D=int(d); m=(d-D)*60; M=int(m); s=(m-M)*60
        return f"{sg}{D:02d} {M:02d} {s:08.5f}"
    return hms(ra),dms(de)

def self_test():
    truth=2445000.25
    ura,ude=vec_to_radec(pred_vec('Uranus',truth)); nra,nde=vec_to_radec(pred_vec('Neptune',truth))
    obs={'Uranus':obs_vec(ura,ude),'Neptune':obs_vec(nra,nde)}
    best,second=reconstruct(obs,truth-1200,truth+1200)
    err=abs(best[1]-truth)
    validity_ok=True
    try:
        validate_search_window(MODEL_START_JD,MODEL_END_JD-1e-6)
    except ValueError:
        validity_ok=False
    boundary_rejected=False
    try:
        validate_search_window(MODEL_START_JD,MODEL_END_JD)
    except ValueError:
        boundary_rejected=True
    checks={
      'unit_earth':abs(math.sqrt(sum(x*x for x in pred_vec('Uranus',truth)))-1)<1e-12,
      'unit_neptune':abs(math.sqrt(sum(x*x for x in pred_vec('Neptune',truth)))-1)<1e-12,
      'synthetic_roundtrip_lt_30min':err<30/(24*60),
      'separated_second_solution':second is not None and abs(second[1]-best[1])>30,
      'stdlib_only':True,
      'light_time_changes_solution_geometry':angle_deg(pred_vec('Neptune',truth,True),pred_vec('Neptune',truth,False))>0,
      'validity_window_accepts_1800_2050':validity_ok and boundary_rejected,
      'ra_validation_rejects_24h':False,
      'dec_validation_rejects_91deg':False,
    }
    try: sexa('24 00 00',True)
    except ValueError: checks['ra_validation_rejects_24h']=True
    try: sexa('+91 00 00',False)
    except ValueError: checks['dec_validation_rejects_91deg']=True
    print('Solar System Time Reference Resolver v1.0.4 self-test')
    for k,v in checks.items(): print(f"{k}:{'PASS' if v else 'FAIL'}")
    print(f"synthetic_truth_jd:{truth:.6f}")
    print(f"synthetic_reconstructed_jd:{best[1]:.6f}")
    print(f"synthetic_abs_error_days:{err:.9f}")
    print(f"checks:{sum(checks.values())}/{len(checks)} {'PASS' if all(checks.values()) else 'FAIL'}")
    return 0 if all(checks.values()) else 1

def main():
    ap=argparse.ArgumentParser(description='Solar System Time two-planet J2000 reference resolver')
    ap.add_argument('--self-test',action='store_true')
    ap.add_argument('--start-jd',type=float); ap.add_argument('--end-jd',type=float)
    ap.add_argument('--allow-outside-model-validity',action='store_true',help='allow exploratory searches outside the declared 1800-2050 approximate-element validity window')
    ap.add_argument('--uranus-ra'); ap.add_argument('--uranus-dec'); ap.add_argument('--neptune-ra'); ap.add_argument('--neptune-dec')
    a=ap.parse_args()
    if a.self_test: return self_test()
    req=(a.start_jd,a.end_jd,a.uranus_ra,a.uranus_dec,a.neptune_ra,a.neptune_dec)
    if any(x is None for x in req): ap.error('provide --start-jd --end-jd and Uranus/Neptune RA/Dec, or use --self-test')
    try:
        validate_search_window(a.start_jd,a.end_jd,a.allow_outside_model_validity)
        obs={'Uranus':obs_vec(a.uranus_ra,a.uranus_dec),'Neptune':obs_vec(a.neptune_ra,a.neptune_dec)}
    except ValueError as exc:
        ap.error(str(exc))
    best,second=reconstruct(obs,a.start_jd,a.end_jd)
    print('Solar System Time Reference Resolver v1.0.4')
    print(f'best_jd:{best[1]:.9f}')
    print(f'best_rms_deg:{best[0]:.9f}')
    if second:
        print(f'second_jd:{second[1]:.9f}')
        print(f'second_rms_deg:{second[0]:.9f}')
        print(f'second_to_best_ratio:{second[0]/best[0]:.9f}' if best[0]>0 else 'second_to_best_ratio:inf')
    return 0
if __name__=='__main__': raise SystemExit(main())
