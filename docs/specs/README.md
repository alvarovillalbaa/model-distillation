# model-distillation specification

Last updated: 2026-11-10

Status: implemented. The README describes the implemented primitive scope; the inherited blueprint includes future work.

## Responsibility

Task/response records, teacher eligibility, verification-result binding and
preference-pair construction. Objective verification execution is owned by
verification-runtime; Open Evals keeps general evaluation composition/scoring.

## First next work

- [ ] Add a teacher registry and response lineage before real generation.
- [ ] Integrate other verifiers through explicit result identities.
- [ ] Keep model training and Open Evals integration optional.

The 0.2 interface consumes verification-runtime results directly. Correctness
does not grant teacher-output rights, and a stale result for changed candidate
or reference bytes is rejected before constructing a pair.

## Interfaces and composition

Use the public package API or CLI documented in the README. There is no import from Lab and no required evaluation service.

[Inherited blueprint](blueprint.md) preserves the relevant original design sections. Provider claims, dates, estimates, and unimplemented features there are historical requirements, not new measurements.

[Inherited backlog](backlog.md) records the original planning status; use the implementation status above for the current boundary.

## Acceptance

Source checks are available with an explicit source root; installation and wheel checks require the storage preflight and are tracked as separate proof.
