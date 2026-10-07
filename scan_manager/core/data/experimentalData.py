from .shot import Shot
import pandas as pd

from laplace_log import log

class ExperimentalData:
    COLUMNS = [
    "shot_num",
    "timestamp",
    "type",
    "device_address",
    "device_name",
    "variable_name",
    "value",
    ]

    def __init__(self):
        self.shots = {}
        self.dataframe = pd.DataFrame(columns=self.COLUMNS)

    def add_shot(self, master_raw_data: dict) -> None:

        shot = Shot.from_master_data(master_data=master_raw_data)
        self.shots[shot.shot_number] = shot

        rows = []

        # -----------------
        # Actuators
        # -----------------
        for address, actuator in shot.actuators.items():
            shot_num = actuator.get("shot_number")
            timestamp = None
            device_name = None

            for motor in actuator.get("motors", []):
                rows.append({
                    "shot_num": shot_num,
                    "timestamp": timestamp,
                    "type": "act",
                    "device_address": address,
                    "device_name": device_name,
                    "variable_name": motor.get("name"),
                    "value": motor.get("position"),
                })

        # -----------------
        # Diagnostics
        # -----------------
        for address, diagnostic in shot.diagnostics.items():
            shot_num = diagnostic.get("shot_number")
            timestamp = diagnostic.get("time")
            device_name = diagnostic.get("name")

            # Everything except metadata is a potential plotted variable
            excluded = {
                "shot_number",
                "name",
                "time",
                "motor",
            }

            for variable_name, value in diagnostic.items():
                if variable_name in excluded:
                    continue

                rows.append({
                    "shot_num": shot_num,
                    "timestamp": timestamp,
                    "type": "diag",
                    "device_address": address,
                    "device_name": device_name,
                    "variable_name": variable_name,
                    "value": value,
                })

        # Append new rows to the main DataFrame
        if rows:
            self.dataframe = pd.concat(
                [self.dataframe, pd.DataFrame(rows)],
                ignore_index=True,
            )


    def plot(self, plot_config: dict)->dict:
        pass

    def save_all_data(self)-> None:
        pass

