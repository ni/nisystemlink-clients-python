---
id: ADR-NNN
date: YYYY-MM-DD
title: <Short decision title>
type: <architectural | implementation | informational>
status: <proposed | accepted | deferred | rejected | superseded>
supersedes: []
---

<!--
Use this template for proposed, accepted, deferred, rejected, and superseded
records. Use decision-needed.md while no direction has been selected.

- File name: ADR-NNN-<slug>.md in the docs/decisions/ directory.
- date: the date the current status or chosen direction was established.
- supersedes: repository-relative decision file paths, not bare IDs.
- Status changes follow the outline in the README.
- Add or update the row in docs/decisions/README.md's index.
-->

# <ID>: <Short decision title>

## Context

<!-- Use short bullets. The first states the problem: what must be decided,
and what goes wrong or stays undecided without a decision. Add one constraint
or force per bullet, with its source and any needed term defined. Don't describe
the chosen solution here. -->

## Decision

<!-- The first bullet states the selected direction plainly. Add bullets for
its parts when needed. For deferred records, state what was deferred. -->

### Rationale

<!-- Explain how the choice meets the Context constraints, cite evidence, and
state assumptions that would reopen the decision. Don't repeat the Decision or
the alternatives' drawbacks. -->

### [Implementation topic] (optional)

<!-- When the decision shapes code, describe the approach the tech lead must
approve: key types and interfaces, data shapes, non-obvious algorithms,
transaction/concurrency/error boundaries, and edge cases. Keep out
method-by-method steps, file lists, and task order. Name this subsection for
what it describes, such as "Claim and recovery". Include only what is needed
to clarify or illustrate the decision, not an implementation plan. -->

## Alternatives Considered

<!-- Optional. Give each realistic option its own bullet, starting with a short
bold name and colon. Explain why it wasn't chosen and any benefit it would
have had, then say when to reconsider it or what rules it out. Delete this
section when no alternatives were weighed. -->

## Consequences

<!-- Record accepted trade-offs, invariants later changes must keep, and
limits. Don't repeat benefits from Rationale. For deferred records, state the
revisit trigger or condition. Use one point per bullet, with short, plain
language. If sections before the implementation subsection run past about a
page, check whether the record bundles separate choices or includes mechanics. -->
