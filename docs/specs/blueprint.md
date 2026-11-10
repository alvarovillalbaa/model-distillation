# Inherited model-distillation blueprint

Last updated: 2026-11-10

Historical design extracted from [Lab at ba67e51](https://github.com/alvarovillalbaa/lab/blob/ba67e510bab2703b1042993744ce099490221c1f/docs/specs/steps.md). The component specification owns current scope. This text does not prove implementation, current provider facts, or executed research.

# 13. Phase 9 — build the advanced distillation system

This is where you can actually innovate.

Do not think of distillation as “ask GPT-4 a bunch of questions and fine-tune.” That is amateur. Build a **data engine**.

## 13.1 Distillation system architecture

```text
Prompt/task generator
        ↓
Teacher registry
        ↓
Multi-teacher response generation
        ↓
Verifier/judge ensemble
        ↓
Preference pair builder
        ↓
Curriculum sampler
        ↓
Student trainer
        ↓
Evaluator/gatekeeper
        ↓
Lineage database
```

## 13.2 Core components

### A. Teacher registry

Track every teacher:

```yaml
teacher_id: qwen_xxx
type: open_weights
license: apache-2.0
allowed_for_distillation: true
strengths:
  - math
  - code
weaknesses:
  - safety
  - long_context
cost_per_1m_tokens: ...
latency: ...
```

Important: only train on teacher outputs when the license or provider terms allow it. Do not assume API outputs are allowed for model training.

### B. Task generator

Generate prompts by domain:

```text
math
code
science
instruction following
tool use
long context
summarization
structured output
safety/refusal
multilingual
```

Task metadata:

```json
{
  "task_id": "math_000123",
  "domain": "math",
  "difficulty": 0.72,
  "source": "synthetic_seed_v4",
  "requires_verifier": true,
  "expected_answer_type": "integer",
  "contamination_checked": true
}
```

### C. Multi-teacher generation

For each prompt:

* sample from 2–5 teachers
* use multiple temperatures
* generate concise and detailed versions
* generate chain-of-thought only when allowed and appropriate
* generate incorrect distractors for preference training
* record all metadata

### D. Verifiers

Use objective verifiers whenever possible:

| Domain    | Verifier                        |
| --------- | ------------------------------- |
| code      | run tests in sandbox            |
| math      | symbolic/numeric checker        |
| JSON      | schema validator                |
| tool use  | environment success             |
| citations | source-span checker             |
| safety    | policy classifier + spot checks |

LLM judges are useful, but never trust only an LLM judge for your core claims.

### E. Preference builder

Create preference pairs:

```text
chosen = verified correct, clear, safe, efficient
rejected = incorrect, verbose, unsafe, hallucinated, formatting failure
```

Also create **hard negatives**:

* plausible but wrong math
* code that passes simple tests but fails hidden tests
* answers with subtle instruction violations
* unsafe over-refusals
* unsafe under-refusals

### F. Curriculum sampler

Train from:

```text
easy → medium → hard
short → long
single skill → composed skill
teacher-generated → student-generated
verified → judge-assisted
```

### G. Student uncertainty sampling

Have the student attempt tasks. Prioritize examples where:

* student is wrong but teacher/verifier is right
* teachers disagree
* student confidence is high but wrong
* reward model uncertainty is high
* eval regression appears in a domain

This makes distillation compute-efficient.

## 13.3 Distillation methods to implement

| Method                            | Use                                                      |
| --------------------------------- | -------------------------------------------------------- |
| SFT distillation                  | basic teacher imitation                                  |
| Logit distillation                | only with open/local teachers where logits are available |
| Preference distillation           | DPO/IPO/KTO from teacher rankings                        |
| Process distillation              | train on verified solution traces                        |
| Rejection sampling                | sample many, keep verified best                          |
| Self-distillation                 | student generates, verifier filters                      |
| Specialist distillation           | math/code/tool/safety specialists                        |
| Router distillation               | route prompts to specialists or train MoE-style router   |
| Speculative decoding distillation | train small draft model for faster serving               |

## 13.4 Research-grade distillation experiments

Run these as controlled ablations:

| Experiment                                              | Hypothesis                                      |
| ------------------------------------------------------- | ----------------------------------------------- |
| single teacher vs multi-teacher                         | teacher diversity improves robustness           |
| LLM judge vs verifier                                   | objective verifiers reduce false positives      |
| random synthetic data vs uncertainty-selected data      | active selection improves eval-per-token        |
| SFT only vs SFT+DPO                                     | preferences improve instruction-following       |
| SFT+DPO vs SFT+GRPO on verifiable tasks                 | RL improves reasoning where reward is objective |
| dense post-training vs specialist modular post-training | specialists reduce capability interference      |

Ai2’s Branch-Adapt-Route work is relevant here: they train domain experts separately, merge into an MoE-style model, and train the router cheaply using a small stratified sample; they report that modular training avoids some cross-domain interference. ([allenai.org][16])

Your novel angle could be:

> “Distillation as an autonomous, verifier-gated, cost-aware curriculum system.”

That is a serious research direction.

---
