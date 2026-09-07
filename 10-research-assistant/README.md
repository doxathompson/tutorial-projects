# Citation-First Research Assistant

An offline retrieval assistant that breaks source documents into passages,
ranks them with BM25, and produces an extractive answer with verifiable source
citations. It intentionally works without an LLM: retrieval and citation
quality should be correct before adding generative complexity.

```bash
python assistant.py ./documents "What are the benefits of testing?"
python -m unittest discover -s tests -v
```

## Next production milestone

Put generation behind a `Generator` interface, pass only retrieved passages to
the model, require citation IDs in its response, reject unknown citations, and
evaluate retrieval recall on a hand-labelled question set. Never treat model
fluency as evidence of correctness.

