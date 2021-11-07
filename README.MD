# COVID-19 Dashboard
This project is part of the **Data Science & Society** group project and is created by **Group 10**. For more details about the project please refer to the project documentation

---

## Run Dashboard with docker

To run the dashboard download this repository, navigate to it and run:

```docker-compose up```

Afterwards you can view the dashboard on localhost (port 80)
**Please note:** The system import data, cleans data and trains models when launching the application. This takes approximetely 5 miuntes.

---
## Code documentation
The codebase can be devided in to two types of code:

**Data processing:** `helpers.py`, `hospitalizations.py`, `measures.py`, `populations.py`, `predictions.py`, `preprocessing_predictions.py`, `temperature.py`, `time_series_prediction.py`, `vaccinations.py`
**Dashboard**:
- **Parts of the website (in order of appearance)**: `header.py`, `current_situation.py`, `cases_overview.py`, `hospitalizations_overview.py`, `vaccinations_overview.py`, `vaccinations_agegroup.py`
- **Configs**: `cases_overview_config.py`, `vaccinations_overview_config.py`
- **Helpers**: `colors.py`, `data_importer.py`, `website_component.py`
The class that all these aforementioned files is `website.py`, and is initalized by `run_website.py` 

## Run dashboard without docker
To run the website **without docker** make sure you have Python 3.9.x installed and install the required libraries in requirements.txt. The method to do this depends on your method of installing python, it should be something like `pip install -r requirements.txt`, `pip3 install -r requirements.txt` or `python3.9 -m pip install -r requirements.txt`
Then run:
```
python3 run_website.py
```
Again, you're python name might differ.

run_website.py can be called with some arguments:
- `-oc` or `--overwrite-cache`: Force the fetching of new data, and train all models again.
- `-dev` or `--debug`: Run the website locally (host on 127.0.0.1 instead of 0.0.0.0), and enable the Debug tools provided by Dash

## Additional info
The system caches data for 6000 seconds, which can help very much to speed up loading (few seconds vs. multible minutes). The files will be downloaded in the `./cache` folder

## Used libraries / Tools
- [**Dash**](https://github.com/plotly/dash) (version 2.0.0): MIT License
- [**Pandas**](https://github.com/pandas-dev/pandas) (version 1.3.4): BSD-3-Clause License
- [**NumPy**](https://github.com/numpy/numpy) (version 1.21.2): BSD-3-Clause License
- [**plotly.py**](https://github.com/plotly/plotly.py) (version 5.3.1): MIT License
- [**Matplotlib**](https://github.com/matplotlib/matplotlib) (version 3.4.3): [license](https://github.com/matplotlib/matplotlib/blob/main/LICENSE/LICENSE) (only for development)
- [**Statsmodels**](https://github.com/statsmodels/statsmodels) (version 0.13.3): BSD-3-Clause License
- [**Seoborn**](https://github.com/mwaskom/seaborn) (version 0.11.2): BSD-3-Clause License (only for development)
- [**scikit-learn**](https://github.com/scikit-learn/scikit-learn) (version 1.0.1): BSD-3-Clause License
