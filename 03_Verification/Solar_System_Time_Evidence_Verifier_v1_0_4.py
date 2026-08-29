#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Solar System Time Ledger & Artifact Integrity Verifier v1.0.4.

This verifies declared project-record fields and selected key-artifact hashes. It does not
validate astronomy, reproduce the blind observational results, or establish
chronological pre-registration.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
EXPECTED={
 'r8e_classification':'R8E_BOUNDED_OBSERVATIONAL_REPLICATION_CLAIM_AUDIT_PASS',
 'r7c_score':'6da9b6029aad28666694066b59bdb501a0829da2bacb8a73192bf04924c39d70',
 'r8c_freeze':'b5247af065fb58600adc39eed47d87d372c36192fc9ee2170a266c9f9553501c',
 'r8c_prediction':'bf4e926d0027ae1a699ac9954d6e6a3f05df9f81c2b0612a4ad50ac55e40705c',
 'r8c_score':'e1f3cc123fa3de6fffd5b5f42b266bd631d367e0c4731c0bfdc19058af238f06',
 'r8d_report':'1fd1a3e1317fdbe689dcc1b8aa894dd7f77f600c312da761b50bff2a18e62ccb',
 'r8e_audit':'887c17ac8d9acf29b5224d4043fe53745c3516a5110fe85a3e758bbd71fd2327',
}
def sha256(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def verify():
 here=Path(__file__).resolve().parent; root=here.parent
 ledger_path=root/'02_Frozen_Evidence'/'Solar_System_Time_Evidence_Ledger_v1_0_4.json'
 manifest_path=root/'03_Verification'/'PACKAGE_ARTIFACT_SHA256SUMS_v1_0_4.txt'
 ledger=json.loads(ledger_path.read_text(encoding='utf-8')); e=ledger['evidence']; b=ledger['claim_boundary']
 checks={
  'project_evidence_status_recorded':ledger['project_evidence_status']=='BOUNDED_OBSERVATIONAL_EPOCH_RECONSTRUCTION_RESULT',
  'r8e_claim_audit_recorded':e['R8E']['classification']==EXPECTED['r8e_classification'],
  'external_reproduction_open':ledger['external_independent_reproduction_complete'] is False,
  'r7c_project_commitment_recorded':e['R7C']['score_sha256']==EXPECTED['r7c_score'],
  'r8c_freeze_project_commitment_recorded':e['R8C']['freeze_sha256']==EXPECTED['r8c_freeze'],
  'r8c_prediction_project_commitment_recorded':e['R8C']['prediction_sha256']==EXPECTED['r8c_prediction'],
  'r8c_score_project_commitment_recorded':e['R8C']['score_sha256']==EXPECTED['r8c_score'],
  'r8d_report_project_commitment_recorded':e['R8D']['report_sha256']==EXPECTED['r8d_report'],
  'r8e_audit_project_commitment_recorded':e['R8E']['audit_sha256']==EXPECTED['r8e_audit'],
  'r7c_24_of_24_recorded':e['R7C']['within_3d']=='24/24',
  'r8c_7_of_7_recorded':e['R8C']['within_3d']=='7/7' and e['R8C']['within_7d']=='7/7',
  'r8d_same_basin_7_of_7_recorded':e['R8D']['same_basin_cases']=='7/7',
  'resolver_epoch_hidden_declared':b['absolute_epoch_supplied_to_inverse_resolver'] is False,
  'resolver_relative_time_hidden_declared':b['relative_within_packet_time_supplied_to_inverse_resolver'] is False,
  'packetization_boundary_declared':b['catalog_time_used_upstream_for_packetization'] is True,
  'no_clock_replacement_claim_declared':b['clock_replacement_claimed'] is False,
 }
 manifest_checks=[]
 for line in manifest_path.read_text(encoding='utf-8').splitlines():
  if not line.strip() or line.lstrip().startswith('#'): continue
  parts=line.split(None,1)
  if len(parts)!=2:
   manifest_checks.append((f"MALFORMED:{line.strip()}",False)); continue
  digest,rel=parts; rel=rel.strip(); path=root/rel
  manifest_checks.append((rel,path.is_file() and sha256(path)==digest))
 checks['current_package_artifact_integrity']=all(v for _,v in manifest_checks)
 print('Solar System Time Ledger & Artifact Integrity Verifier v1.0.4')
 print('scope:project ledger consistency + selected key-artifact integrity')
 print('scientific_validation:false')
 print('external_timestamp_proof:false')
 for k,v in checks.items(): print(f"{k}:{'PASS' if v else 'FAIL'}")
 for rel,v in manifest_checks: print(f"artifact:{rel}:{'PASS' if v else 'FAIL'}")
 print(f"checks:{sum(checks.values())}/{len(checks)} {'PASS' if all(checks.values()) else 'FAIL'}")
 print('current_package_status:BOUNDED_OBSERVATIONAL_EPOCH_RECONSTRUCTION_RESULT')
 print('project_evidence_status:'+ledger['project_evidence_status'])
 print('r8e_project_record:'+e['R8E']['classification'])
 print('independent_third_party_reproduction:OPEN_NOT_YET_CONFIRMED')
 return 0 if all(checks.values()) else 1
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--verify',action='store_true',required=True); ap.parse_args(); return verify()
if __name__=='__main__': raise SystemExit(main())
