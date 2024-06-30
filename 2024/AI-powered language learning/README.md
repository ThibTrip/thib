# Description

Here are all the resources of my presentation at the [second Python User Group Freiburg meetup at JobRad](https://www.meetup.com/python-user-group-freiburg/events/301044966/) (2024-06-04).

See slides in file `AI-Powered Language Learning.pdf` and see demos mentioned in the slides in folder `demos` (see also setup below).

# Setup for running the demos

1. Install `poetry` and `jupyterlab`
2. Move to folder `demo_1_and_2` and install the corresponding environment and kernel:

   ```
   poetry install
   poetry run python -m ipykernel install --user --name asr
   ```

3. Move to folder `demo_3` and install the corresponding environment and kernel:

   ```
   poetry install
   poetry run python -m ipykernel install --user --name chatgpt
   ```
