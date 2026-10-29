# Decision records

This directory records durable choices and why they were made. Use it for
compatibility promises, architectural boundaries, and implementation decisions
that future changes need to understand, not routine coding details or task lists.
All records share one repository-wide index and `ADR-NNN` sequence.

## Finding applicable decisions

Before designing or changing behavior, scan the index for relevant topics and
open the linked records. Search record titles and bodies when the summary is
not enough. The record is authoritative; the index is a discovery aid.

Accepted records govern future work once merged to `master`. Other statuses
preserve context, not implementation instructions. A PR can implement the
decision it records, with acceptance reviewed alongside that implementation.
Specifications, public contracts, and tests still define product behavior.
If they conflict with a record, two accepted records conflict, or work depends
on an unresolved choice, report the conflict and obtain a maintainer decision
rather than silently choosing a direction.

## Creating a record

1. Search for an existing record about the question before allocating an ID.
   Resolve an existing undecided record in place; do not duplicate it.
2. Use the next unused number after the highest existing `ADR-NNN`. Never reuse
   an ID, including one belonging to a rejected or superseded record.
3. Copy [decision.md](templates/decision.md) when a direction has been selected,
   or [decision-needed.md](templates/decision-needed.md) when it has not.
   Save it as `ADR-NNN-<lowercase-slug>.md` directly in this directory.
4. Fill the metadata and sections, match the H1 to the ID/title, and remove
   instructional comments and unused optional sections. Use the date the status
   or chosen direction was established, not the date of an editorial correction.
5. Keep one independently changeable decision per record. State the problem
   and constraints in Context, the choice in Decision, why it fits in Rationale,
   and accepted trade-offs and limits in Consequences. Cite evidence and identify
   assumptions that would reopen the choice. Record the maintainer's rationale
   when it comes from discussion rather than a checked-in source.
6. Describe only significant interfaces, data shapes, or error/concurrency
   boundaries in an optional implementation subsection. Leave file lists,
   task order, and method-by-method instructions in the implementation plan.
7. Search existing documentation and code for both the new direction and the
   values it replaces. Reconcile contradictions explicitly. Link the record from
   relevant contributor/user documentation rather than copying its rationale.
8. Add or update the index row in the same PR and obtain normal maintainer review.

## Status and lifecycle

| Status | Meaning |
| --- | --- |
| `decision-needed` | A question needs human judgment; no direction has been selected. |
| `blocked` | The question cannot progress until a named decision or external dependency resolves. |
| `proposed` | A direction is selected for discussion but not accepted. |
| `accepted` | The maintainer has selected this direction; merging the record makes it governing. |
| `deferred` | The choice is deliberately postponed; Consequences names a revisit trigger. |
| `rejected` | The proposed direction was declined; retain the reasoning. |
| `superseded` | A newly accepted record replaces this one. |

Use the undecided template for `decision-needed` and `blocked`; use the decision
template for all other statuses. A recommendation or review comment alone does
not accept a decision. State the intended status explicitly in the PR and have
the maintainer confirm it through review.

- **Clarify in place** for corrections, additional evidence, or wording that
  does not change the required behavior. Keep the original date.
- **Resolve an undecided record** in place when a direction is selected. Preserve
  its original context and resolved question; replace Question, Options, and
  Blocking Dependencies with Decision and Consequences. Remove `blocked_by`.
- **Supersede** when the approach, compatibility promise, or material trade-off
  changes. Create a new record with `supersedes` listing the old record's
  repository-relative path. Only mark the old record `superseded` when the new
  one becomes `accepted`, in the same change; preserve the old reasoning.
- Update the date whenever the status or direction changes. Update the index
  for changes to metadata, summary, or supersession. Keep IDs and paths stable.

## Review checklist

- Metadata, filename, heading, and index agree; IDs are unique.
- Links resolve and `supersedes` contains file paths, not bare IDs.
- Context identifies the problem and sources without presenting the solution.
- The choice, rationale, alternatives actually weighed, and consequences are
  distinct and concise. Deferred/blocked records name their revisit conditions
  or dependencies.
- No placeholder text, guidance comments, conflicting active decisions, or
  implementation task lists remain in a completed record.

## Index

| ID | Date | Status | Type | Summary | Superseded by |
| --- | --- | --- | --- | --- | --- |
| [ADR-001](ADR-001-python-specific-pandas-majors.md) | 2026-10-29 | `accepted` | implementation | Retain pandas 2 below Python 3.15; use native pandas 3 behavior on Python 3.15+ without forcing NbExec image upgrades. | |
