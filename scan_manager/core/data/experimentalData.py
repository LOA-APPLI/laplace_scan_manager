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
        row = shot.data_line()
     
        if shot:
            if self.dataframe.empty:
                self.dataframe = pd.DataFrame({k: [v] for k, v in row.items()})
                log.info(f'Dataframe was empty, columns: {self.dataframe.columns}')
            else:
                self.dataframe.loc[len(self.dataframe)] = shot.data_line()
                log.info(f'Dataframe columns: {self.dataframe.columns}')

    def clear(self) -> None:
        self.dataframe = pd.DataFrame()
        self.shots = {}

    def save_all_data(self)-> None:
        pass

