# model-distillation

Last updated: 2026-11-10

Construct verifier-gated preference data from explicitly permitted teacher responses.

**Status: implemented.** A standard-library Python 3.11+ library and CLI are present. Wheel construction and independent installation passed on Python 3.14.7; see the [installed acceptance receipt](docs/results/2026/11-10/installed-package.json).

## Independent use

From this repository:

```sh
python3 -m pip install .
python3 -m model_distillation.cli demo
python3 examples/quickstart.py
```

No sibling checkout, GPU, account, database, or network service is needed for these examples.

## Ownership

Task/response records, exact-match verification, eligibility gates, and preference-pair construction.

Outside this component: Teacher inference, a training engine, a general evaluation platform, or legal license approval.

## Compose

Use independently, or register a pinned version in [Lab](https://github.com/alvarovillalbaa/lab). A dependency on Lab is never required. Libraries connect through declared dependencies or explicit artifact/job interfaces.

[Specification and next work](docs/specs/README.md) · [Extraction provenance](docs/sources/lab-provenance.json)

MIT applies to the code and authored documentation in this repository. External datasets, model weights, provider services, and third-party projects retain their own terms.

The demo uses authored fixture responses and makes no model call. `allowed_for_distillation` is a caller assertion; it does not establish legal rights. Pair construction requires eligible responses and a verification result bound to the chosen task/teacher. It does not independently prove the verifier is correct.
