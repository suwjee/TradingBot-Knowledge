---
id: "version.current"
type: "version"
status: "active"
authority: "executable"
title: "Current Engine and Reference identities"
version: "5.4.19-EX1"
related_entities: ["source.reference_consistency", "source.reference_registry", "source.source_manifest"]
source_reference: []
evidence_basis: "Latest explicit rebuild requirements and current operating rules"
---

# Current version and exact identity

Freshly re-audited 2026-09-29 (Asia/Tehran); original byte capture was 2026-09-28 22:42:47 +0330. Canonical Reference version: 5.4.19-EX1. This is current audited dirty working-tree evidence; HEAD is provenance metadata.

| Current Source | Module version | Implementation version | SHA-256 |
|---|---|---|---|
| engine/__init__.py | unversioned package marker | not separately declared | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| engine/bridge/__init__.py | unversioned package marker | not separately declared | 2bc59770b9d4313c0e6306287d074487b9e1672dbaf3ada9a8be381e7123f0b8 |
| engine/bridge/trading_pipeline.py | 1.7.0 | 1.8.0 | ef5109f4ebb95bc0e04b3d964b14da5f764ae4472f3d10a1a9b7192d59fec683 |
| engine/pipeline/__init__.py | unversioned package marker | not separately declared | ca549e4cf5d9a070227498d0d210279e0f7edae66d62dadab7981cddaa1db5c3 |
| engine/pipeline/a_zone_detector.py | 1.6.4 | not separately declared | d7c33dd619ad7e4590027667a2c4e984c83be7b82fbfafeb5d7f944ddd521097 |
| engine/pipeline/blue_line_detector.py | 2.3.0 | not separately declared | 6fa01d94bc98060b62bc7e68db0ec24a0b0159727d44043affee7130a9c11448 |
| engine/pipeline/core_utils.py | 1.0.0 | not separately declared | 3dae390ae77b72965f5799f7c132c4eba203775d5e72761fd7dd60c90f8578de |
| engine/pipeline/direction_policy.py | 1.0.0 | not separately declared | a27ac63c2f066311c9381e2ead6fb44f0789f423a37b465da65c80e6329397ea |
| engine/pipeline/e_zone_detector.py | 6.16.1 | 6.18.1 | 38834e96cc58931fe2e12096f4465ecaa046387d30fd40fecbd6891971020988 |
| engine/pipeline/lifecycle_engine.py | 1.17.0 | 1.18.0 | 94feb038e1e78b291762cfc03dfc370e48bb94f3e1fe1171b7a5206301e8be13 |
| engine/pipeline/order_audit_engine.py | 1.5.1 | not separately declared | 09cba00c0623ffcce0d7bc3460c1e963c4e2b14fb02a9172cc25dcca8ba9aedc |
| engine/pipeline/reaction_engine.py | 9.8.0 | not separately declared | bea0d5a5e95ee15ad54d024f6c01b8c777ba2abcc3c8e671118f1ae2df28f2a6 |
| engine/pipeline/s_zone_detector.py | 4.20.0 | 4.21.0 | ef71a2e4176caaabc25d1ef0c1f0f24efb54ed3110982cdb7cf52d2449cca2ee |

| Direction | Current Reference SHA-256 | Bytes |
|---|---|---:|
| Bearish | 109753d7d056b6b9ee173cc7f47472b53a77174d26e89f38b00b81061f310e18 | 569305 |
| Bullish | d3a0b89c59f1304ddefe6f6931cedf7ea2e17a15893c63d652c89489f3e6387f | 569275 |

RAW and Fixtures are EMPTY_BY_DESIGN. Market regression is NOT_REQUIRED_THIS_PHASE. Read the current validation report for structural readiness.
