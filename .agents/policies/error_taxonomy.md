# Error Taxonomy

Every pipeline failure MUST use exactly one class:

- PARSER
- NORMALIZER
- TRANSLATOR
- FORMATTER
- LATEX
- COMBINE
- COMPILE
- PDF
- RUNTIME

Forbidden classes: Unknown, Misc, Other.

Rule: classify the layer that produced the defect, not the layer that observed it.
