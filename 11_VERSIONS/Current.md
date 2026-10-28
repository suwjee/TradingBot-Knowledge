---
id: "version.current"
type: "version"
status: "active"
authority: "executable"
title: "Current Engine and Reference identities"
version: "5.4.33"
related_entities: ["source.reference_consistency", "source.reference_registry", "source.source_manifest"]
source_reference: []
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
last_modified_at: "2026-10-27T20:18:37+03:30"
---
# Current captured version and identity

Captured during the 2026-10-27 live review. Accepted Reference document identity is 5.4.33; module API and implementation versions remain independent. Source commit c2e7903890dddfaf8526cb9b11dd1c5e490c7410 supplies provenance only. Current project bytes, not a version label, identify executable behavior.

The recursively discovered in-scope production owners and package markers are exact snapshots. The explicitly excluded added detector has no standalone snapshot or concept node. Its payload is retained only inside complete exact accepted References with embedded-only integrity pins. Consequently this Code tree is intentionally not a full standalone runnable Engine reconstruction.

| Source | Module version | Implementation version | SHA-256 |
| --- | --- | --- | --- |
| engine/__init__.py | unversioned package marker | not separately declared | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| engine/bridge/__init__.py | unversioned package marker | not separately declared | 2bc59770b9d4313c0e6306287d074487b9e1672dbaf3ada9a8be381e7123f0b8 |
| engine/bridge/trading_pipeline.py | 1.11.0 | 1.14.2 | d70481975d2b8e41c6271a02243862d967d5c906bbe1f2f23a432df6fc0f85a1 |
| engine/pipeline/__init__.py | unversioned package marker | not separately declared | d22a1b81495a6c97b5eccc4d921b1ba4b709bfbcd39be6ef34b9014690b9f460 |
| engine/pipeline/a_zone_detector.py | 1.7.0 | not separately declared | 83f08b06556eb59c6d1b3afd22b51c280315bd80f3a31bc3044ada349251a115 |
| engine/pipeline/blue_line_detector.py | 2.4.1 | not separately declared | c6466c280504f82d8f2b189263ed0e9b9581c2f48edd8aaa12f016e55effc98c |
| engine/pipeline/core_utils.py | 1.0.0 | not separately declared | 007e5329e14ab9695e555c630527badc84dd35a239dea1cf685141e4278265eb |
| engine/pipeline/direction_policy.py | 1.0.0 | not separately declared | a27ac63c2f066311c9381e2ead6fb44f0789f423a37b465da65c80e6329397ea |
| engine/pipeline/e_zone_detector.py | 6.16.2 | 6.18.5 | 96ea351ff88c195937da5c32c5712356b9b876ba6f509d68cb16d37012958ad5 |
| engine/pipeline/lifecycle_engine.py | 1.18.6 | 1.20.7 | 760928f5480efad446b42bc6aa2fbea3e431de13ab92714bac05c09188519c26 |
| engine/pipeline/order_audit_engine.py | 1.7.1 | not separately declared | f4e991a6a516ad84e0223c802f5baf611f5e20fb8d7965b9dcdf4ff949d89296 |
| engine/pipeline/reaction_engine.py | 9.8.1 | 9.9.1 | f62f7e3c6480750068c4550a8489806030aac16f021f349930bd5efb3ce54198 |
| engine/pipeline/s_zone_detector.py | 4.20.1 | 4.21.1 | 0c5864bc3bc6c17f72c5c38b04a1cd0b5b38c726d8834207a55d5351fdfa38fe |

| Direction | Exact local Reference | SHA-256 | Bytes |
| --- | --- | --- | ---: |
| Bearish | 06_SOURCE/Code/engine/algorithms/TradingBot_Bearish_Algorithm_Reference_V5.4.33_Source_Synchronized.md | bfb201d3d6b4d4d52fcd28ef6b8d77918757d5ed14fe8df033d9abfd4d499baf | 743552 |
| Bullish | 06_SOURCE/Code/engine/algorithms/TradingBot_Bullish_Algorithm_Reference_V5.4.33_Source_Synchronized.md | 131a0edb6945a59f4161c12aa00ba2c4cf5f787840a3786dbc66b5b3e69b27f7 | 743524 |

RAW/fixture stores remain EMPTY_BY_DESIGN. Market regression is NOT RUN for this knowledge refresh. See _GENERATED/Current-Validation.md for completed structural/contract gates and declared exclusions.
