# This is the component on which is the base of all other website components. The function allows each component to store the chosen data to the self.data dict

from datetime import datetime


class Website_Component:
    def __init__(self):
        pass

    def store_required_data(self, data: dict, keys: list, start_date: datetime=None):
        # Data is a dict of full df's
        self.data = {}
        for k in keys:
            if start_date:
                self.data[k] = data[k][data[k]['date'] >= start_date]
                continue
            self.data[k] = data[k]