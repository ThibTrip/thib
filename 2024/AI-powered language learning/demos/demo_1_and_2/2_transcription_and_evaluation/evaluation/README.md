# Protocol

1. Download the [common voices data](https://commonvoice.mozilla.org/en/datasets) set from Mozilla for a given language
2. Unpack the folder containing `clips` and the various datasets, e.g. `it` for the italian dataset and `uk` for the Ukrainian dataset
3. Run notebook `1_select_random_clips.ipynb` to select random clips and put it in a new local databse `cv.sqlite3`
4. Run notebook `2_transcribe.ipynb` for preparing transcriptions to evaluate the different automatic speech recognition tools (e.g. `Whisper large-v3` and Google API Speech v2 via `autosub`)
5. Run notebook `3_evaluate_models.ipynb` for evaluating models
