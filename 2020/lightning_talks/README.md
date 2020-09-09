# Presentation on packaging

* Link to the [presentation](https://thibtrip.github.io/lightning_talks/#/)
* Link of the [meetup](https://www.meetup.com/fr-FR/Python-User-Group-Freiburg/events/267885800/) in Freiburg during which I presented

# Creating slides from the notebook

We assume you already have Jupyter Lab or Jupyter Notebook installed. If that is not the case I recommand installing it by [installing Anaconda](https://docs.anaconda.com/anaconda/install/).

```
pip install -r requirements.txt
jupyter nbconvert lightning_talks.ipynb --to slides --SlidesExporter.reveal_scroll=True --reveal-prefix "https://cdn.jsdelivr.net/npm/reveal.js@3.6.0" --execute --SlidesExporter.reveal_theme=white
python ../../embed_images.py lightning_talks.slides.html
```
