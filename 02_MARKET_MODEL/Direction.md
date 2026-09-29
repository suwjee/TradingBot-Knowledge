---
id: "market.direction"
type: "market"
status: "active"
authority: "executable"
title: "Current direction primitives"
version: "current"
related_entities: []
source_reference: ["06_SOURCE/Code/engine/pipeline/direction_policy.py"]
evidence_basis: "Current source and synchronized current references"
direction_sensitivity: "mixed: geometry changes, native chronology and identity remain invariant"
name: "Direction"
aliases: ["Bullish and Bearish"]
---

# Current direction primitives

Bullish policy chooses low as directional extreme, high as opposite extreme, First RED and GREEN context. Bearish chooses high, low, First GREEN and RED context. strict_cross and better_extreme use Bullish < and Bearish >. choose_extreme uses min/max. Confirmation uses Bullish > and Bearish < on already selected confirmation-side prices.
