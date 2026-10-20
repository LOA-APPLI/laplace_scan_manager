from .shot import Shot
import pandas as pd

from laplace_log import log

class ExperimentalData:

    def __init__(self):
        self.shots = {}
        self.dataframe = pd.DataFrame()

    def add_shot(self, master_raw_data: dict) -> None:

        shot = Shot.from_master_data(master_data=master_raw_data)
        self.shots[shot.shot_number] = shot
        if shot:
            log.info(f'Data line: {shot.data_line()}')


    def save_all_data(self)-> None:
        pass

