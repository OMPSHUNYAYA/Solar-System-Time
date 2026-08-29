SOLAR SYSTEM TIME — VERIFICATION v1.0.4

Active verifier:
Solar_System_Time_Evidence_Verifier_v1_0_4.py

Run:
python -B Solar_System_Time_Evidence_Verifier_v1_0_4.py --verify

Scope
-----
Despite the historical filename stem, this is a ledger and artifact integrity
verifier. It checks:
- declared fields in the machine-readable historical evidence ledger;
- recorded project commitment hashes;
- selected key-artifact hashes for the resolver, frozen machine-readable evidence,
  verifier, interactive clock, and clock verifier.

It does NOT:
- reproduce the 24/24 or 7/7 observational results;
- validate celestial-mechanics accuracy;
- provide outside peer review or certification;
- prove that historical prediction hashes existed before truth reveal using an
  independently controlled timestamp.

The SHA-256 manifest deliberately excludes editable narrative, licensing, notice,
and repository-navigation files. This keeps integrity commitments focused on the
computational and machine-readable evidence anchors while allowing ordinary
documentation maintenance without invalidating the key-artifact manifest.

This distinction is intentional and should be preserved in derived packages.
