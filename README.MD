# COVID-19 Dashboard
This project is part of the ** Data Science & Sociaty ** group project and is created by ** Group 10 **

---

## Run Dashboard with docker

To run the dashboard download this repository, navigate to it and run:

```docker-compose up```

Afterwards you can view the dashboard on localhost (port 80)
**Please note: ** The system import data, cleans data and trains models when launching the application. This takes approximetely 5 miuntes.

---
# Code documentation
The codebase can be devided in to two types of code:
** Data processing: ** `helpers.py`, `hospitalizations.py`, `measures.py`, `populations.py`, `predictions.py`, `preprocessing_predictions.py`, `temperature.py`, `time_series_prediction.py`, `vaccinations.py`
** Dashboard **:
- ** Parts of the website (in order of appearance)**: `header.py`, `current_situation.py`, `cases_overview.py`, `hospitalizations_overview.py`, `vaccinations_overview.py`, `vaccinations_agegroup.py`
- ** Configs **: `cases_overview_config.py`, `vaccinations_overview_config.py`
- ** Helpers **: `colors.py`, `data_importer.py`, `website_component.py`
The class that all these aforementioned files is `website.py`, and is initalized by `run_website.py` 

## Run dashboard without docker
To run the website ** without docker ** make sure you have Python 3.9.x installed and install the required libraries in requirements.txt. The method to do this depends on your method of installing python, it should be something like `pip install -r requirements.txt`, `pip3 install -r requirements.txt` or `python3.9 -m pip install -r requirements.txt`
Then run:
```
python3 run_website.py
```
Again, you're python name might differ.

run_website.py can be called with some arguments:
- `-oc` or `--overwrite-cache`: Force the fetching of new data, and train all models again.
- `-dev` or `--debug`: Run the website locally (host on 127.0.0.1 instead of 0.0.0.0), and enable the Debug tools provided by Dash

# Additional info
The system caches data for 6000 seconds, which can help very much to speed up loading (few seconds vs. multible minutes). The files will be downloaded in the `./cache` folder
