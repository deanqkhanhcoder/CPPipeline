---
name: fragment-qa
description: Validate LaTeX fragments before combine. Reject bad fragments and force correct-layer regeneration; never repair output.tex/PDF.
---

## Declarative Dependencies
- **Runtime**: `.agents/runtime/runtime.md`
- **Policies**: `.agents/policies/repository_policy.md`, `.agents/policies/template_policy.md`, `.agents/policies/error_taxonomy.md`
- **Knowledge**: `.agents/knowledge/root_causes.md`
- **Required Skills**: None
- **Optional Skills**: None
- **Optional Knowledge**: None

# Fragment QA

Host LLM is the runtime. This skill gates every `cache/build/<id>.tex` before combine.

## Contract

Input: LaTeX fragment(s).
Output: PASS or FAIL with one error class:
PARSER, NORMALIZER, TRANSLATOR, FORMATTER, LATEX, COMBINE, COMPILE, PDF, RUNTIME.

Forbidden classes: Unknown, Misc, Other.

## Quy tr?nh th?c thi

1. Run `python tools/fragment_qa.py <fragment-or-cache/build>`.
2. If PASS: allow combine.
3. If FAIL:
   - identify producer layer,
   - reject fragment,
   - regenerate from that layer,
   - rerun Fragment QA.

## Never

- never patch `outputs/output.tex`
- never patch `outputs/output.pdf`
- never create `fix_output*.py`
- never regex-repair a generated artifact
- never combine a failing fragment
