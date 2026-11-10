# model-distillation

Last updated: 2026-11-10

Construct verifier-gated preference data from explicitly permitted teacher responses.

**Status: implemented.** Version 0.2 is a Python 3.11+ library and CLI with an
explicit pinned verification-runtime dependency. The
[0.1 installed receipt](docs/results/2026/11-10/installed-package.json) is
historical; acceptance for this extraction is recorded separately in Lab.

## Independent use

From this repository:

```sh
python3 -m pip install .
python3 -m model_distillation.cli demo
python3 examples/quickstart.py
```

No sibling checkout, GPU, account, database, or network service is needed for these examples.

## Ownership

Task/response records, teacher eligibility, verification-result binding and
preference-pair construction. Objective answer checking belongs to
[verification-runtime](https://github.com/alvarovillalbaa/verification-runtime).
Import its `VerificationResult` and `verify_exact_match` directly; version 0.2
removes those old model-distillation exports.

Outside this component: Teacher inference, a training engine, a general evaluation platform, or legal license approval.

## Compose

Use independently, or register a pinned version in [Lab](https://github.com/alvarovillalbaa/lab). A dependency on Lab is never required. Libraries connect through declared dependencies or explicit artifact/job interfaces.

[Specification and next work](docs/specs/README.md) · [Extraction provenance](docs/sources/lab-provenance.json)

MIT applies to the code and authored documentation in this repository. External datasets, model weights, provider services, and third-party projects retain their own terms.

The demo uses authored fixture responses and makes no model call.
`allowed_for_distillation` is a caller assertion; it does not establish legal
rights. Pair construction requires eligible responses and a result bound to
the task ID, original chosen-response bytes and expected-reference bytes.
It does not independently authenticate the verifier or establish its correctness.
