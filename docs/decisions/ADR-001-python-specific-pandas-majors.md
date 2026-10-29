---
id: ADR-001
date: 2026-10-29
title: Use Python-specific pandas majors
type: implementation
status: accepted
supersedes: []
---

# ADR-001: Use Python-specific pandas majors

## Context

- Adding Python 3.15 support requires deciding which pandas major to install
  and whether DataFrame helpers should preserve older pandas defaults.
  Without a policy, dependency resolution and output expectations are ambiguous.
- [pandas 2.3.3's published artifacts](https://pypi.org/pypi/pandas/2.3.3/json)
  have no CPython 3.15 wheels. Local Python 3.15 validation of that version
  crashed when constructing a timestamp column; pandas 3.1 completed the same
  operation and [provides 3.15 wheels](https://pypi.org/pypi/pandas/3.1.0/json).
- The repository maintainer established during this maintenance that a global
  pandas major upgrade would also require upgrading NbExec (notebook execution)
  image versions, a customer-facing disruptive change. Those image upgrades
  are outside this repository's Python-support maintenance.
- DataFrame tests currently assume pandas 2 timestamp units and missing-value
  comparisons. pandas 3 changes timestamp-unit inference, inferred string
  dtypes, and some missing-value behavior.

## Decision

- Retain pandas 2 on Python 3.11-3.14 and use pandas 3.1 or later within major 3
  on Python 3.15 and later, expressed as Python-specific dependency constraints.
- Let DataFrame helpers use their installed pandas version's native defaults;
  do not emulate pandas 2 output on Python 3.15.
- Do not upgrade existing NbExec images as part of this maintenance.

### Rationale

- The Python boundary confines the necessary major migration to the newly
  supported runtime without forcing it into existing notebook environments.
  This directly addresses the maintainer's NbExec deployment constraint.
- Native pandas behavior avoids a compatibility layer for dtype and missing
  value inference. Tests must verify exact values, structure, and dtypes for
  the installed major rather than suppress differences.
- Revisit the split when NbExec images can adopt pandas 3 through a coordinated
  customer-facing rollout, or when security or Python support makes pandas 2
  untenable.

## Alternatives Considered

- **Upgrade all supported Python versions to pandas 3:** a single major would
  simplify testing, but would require the disruptive NbExec image migration.
  Reconsider with a coordinated image rollout.
- **Emulate pandas 2 output on Python 3.15:** would reduce output differences
  across runtimes, but adds normalization and maintenance that this decision
  explicitly avoids. Reconsider if a concrete consumer contract requires it.
- **Defer Python 3.15 support:** would avoid the immediate dependency migration,
  but would miss the goal of covering all stable, non-EOL CPython releases.
  Reconsider only if compatible dependencies cannot support that runtime.

## Consequences

- The lock and CI must exercise both pandas majors. Keep the Python-specific
  constraints aligned with the documented support window.
- Consumers moving to Python 3.15 can observe microsecond rather than nanosecond
  timestamp dtypes for these inputs, inferred string rather than object dtypes,
  and different missing-value representations. Do not promise uniform pandas
  inference across runtimes.
- DataFrame tests retain strict dtype/value comparisons using each supported
  major's expectations; omitted fields and explicit nulls remain distinct inputs.
- Future Python 3.x releases remain installable under the package's permissive
  Python constraint, but are not certified until added to the test matrix.
