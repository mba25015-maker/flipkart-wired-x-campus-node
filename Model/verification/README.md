# Verification snapshots

The repository does not redistribute the source PowerPoint or paid research documents. These snapshots preserve only the authored text required for consistency checks.

- `HANDOFF_snapshot.md` supports `verify_docs.py`.
- `DECK_SPEC_snapshot.md` and `PPT_BUILD_PROMPT_snapshot.md` support `verify_spec.py`.
- `deck_text_snapshot.json` contains text extracted from the eight-slide passing deck and its SHA-256 fingerprint; it supports the public default mode of `verify_deck.py`.

To check a newer local artifact, pass its path explicitly:

```bash
python3 Model/verify_docs.py "/path/to/HANDOFF.md"
python3 Model/verify_spec.py "/path/to/DECK_SPEC_SemiFinal.md"
python3 Model/verify_deck.py "/path/to/submission.pptx"
```

The snapshots demonstrate consistency with the packaged model at the recorded point in time. They are not substitutes for verifying the final submitted artifact after any edit.

