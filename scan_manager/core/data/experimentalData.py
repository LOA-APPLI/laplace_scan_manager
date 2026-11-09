
from .shot import Shot
from ...data_saver.Data_Classes import HDF5Database

import pandas as pd
from laplace_log import log


class ExperimentalData:

    def __init__(self):
        self.shots = {}
        self.dataframe = pd.DataFrame()
        self.database = HDF5Database("database.h5")

    def add_shot(self, master_raw_data: dict) -> None:

        shot = Shot.from_master_data(master_raw_data)

        if shot is None:
            log.warning("Could not construct Shot")
            return

        self.shots[shot.shot_number] = shot

        row = shot.data_line()

        if not row:
            log.warning(f"No valid data for shot {shot.shot_number}")
            return

        # Append new row
        self.dataframe = pd.concat(
            [self.dataframe, pd.DataFrame([row])],
            ignore_index=True
        )

        # Save both representations
        self.database.save(shot, self.dataframe)

        log.info(f"Saved shot {shot.shot_number}")

    def clear(self) -> None:
        self.dataframe = pd.DataFrame()
        self.shots = {}
