import cases
import vaccinations
import hospitalizations
import measures
import temperature
import sys
import time
import os
import pandas as pd

CACHE_TTL = 6000 #in seconds

class Data_Importer:
    def __init__(self, no_cache:bool=False):
        self.data = {}
        self.overwrite_cache = no_cache
        self.progress = 0
        self.max_progress = 14
    
    def get_data(self):
        loaded_from_cache = self.check_cache()
        if (self.overwrite_cache):
            print('Cache overwrite enabled, downloading new data...')
        else: 
            if (loaded_from_cache):
                print('Loaded data succesfully from cache')
                return self.data
            print('Unable to load data from cache, downloading new!')
        self.update_progress()
        self.data['cases_nl'] = cases.get_cases_df_nl()
        self.update_progress()
        self.data['cases_il'] = cases.get_cases_df_il()
        self.update_progress()
        self.data['cases_nsw'] = cases.get_cases_df_nsw()

        self.update_progress()
        self.data['vaccinations_nl'] = vaccinations.get_vaccinations_df_nl()
        self.update_progress()

        self.data['vaccinations_il'] = vaccinations.get_vaccinations_df_il()
        self.update_progress()
        self.data['vaccinations_nsw'] = vaccinations.get_vaccinations_df_nsw()

        self.update_progress()
        self.data['hospitalizations_nl'] = hospitalizations.get_hospitalizations_df_nl()
        self.update_progress()
        self.data['hospitalizations_il'] = hospitalizations.get_hospitalizations_df_il()
        self.update_progress()
        self.data['hospitalizations_nsw'] = hospitalizations.get_hospitalizations_df_nsw()

        self.update_progress()
        self.data['measures'] = measures.get_measures_df_il_nl_nsw()
        self.update_progress()
        self.data['temperature_nl'] = temperature.get_temperatures_df_nl()
        self.update_progress()
        self.data['temperature_nsw'] = temperature.get_temperatures_df_nsw()
        self.update_progress()
        self.data['temperature_il'] = temperature.get_temperatures_df_il()
        self.update_progress()

        self.write_cache()
        self.overwrite_cache = False
        return self.data

    def check_cache(self):
        load_from_cache = None
        try:
            f = open('./cache/timestamp.txt')
            if (int(f.read()) > time.time() - CACHE_TTL):
                load_from_cache = True
        except: 
            load_from_cache = False
        if (not load_from_cache):
            return False
        self.load_cache()
        return True

    def load_cache(self):
        files = os.listdir('./cache')
        for f in files:
            if (f == 'timestamp.txt'): continue
            self.data[f.split('.')[0]] = pd.read_pickle('./cache/' + f)

    def write_cache(self):
        self.clear_cache()
        os.mkdir('./cache')
        for key in self.data:
            self.data[key].to_pickle('./cache/' + key + '.pkl')
        with open('./cache/timestamp.txt', 'w') as f:
            f.write(str(int(time.time())))

    def clear_cache(self):
        try:
            files = os.listdir('./cache')
        except:
            return
        for f in files:
            os.remove('./cache/' + f)
        os.rmdir('./cache')

    def update_progress(self):
        self.progress += 1
        finishedPart = int(self.progress / self.max_progress * 100 / 2)
        if (self.progress == 100): 
            sys.stdout.write('\r Importing / fetching website data [Done!]                                ')
        sys.stdout.write('\r Importing / fetching website data [{0}] {1}%'.format(('#'*int(finishedPart)) + (' '*(50-finishedPart)), finishedPart * 2))
