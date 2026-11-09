import h5py


class H5Builder:
    """
    To create the file structure, takes a list of anything with a name attribute, and a dict as data.

    """
    def __init__(self, file: str):
        self.file = file

    def _create_file_structure(self, devices: list):
        with h5py.File(self.file, 'a') as f:

            for device in devices:
                f.create_group(device.name)
                self._create_dataset_from_config(device, f)

    def _create_dataset_from_config(self, device, f: h5py.File):
        f.create_dataset(
            name=device.name,
            shape=(0, 2),  # Start with 0 rows, 2 columns
            maxshape=(None, 2),  # Unlimited rows
            dtype='f8',  # float64 for both timestamp and value
            chunks=(1000, 2),  # Chunk size for efficient I/O
            compression='gzip',  # Optional: compress data
            compression_opts=4
        )


import h5py
import numpy as np
import pandas as pd
from urllib.parse import quote
from ..core.data.shot import Shot


class HDF5Database:

    def __init__(self, filename: str = "database.h5"):
        self.filename = filename

    @staticmethod
    def _safe_name(name: str) -> str:
        """Convert a name into a safe HDF5 path component."""
        return quote(str(name), safe="")

    @staticmethod
    def _write_value(group, name, value):

        """Write a scalar value as an HDF5 dataset."""

        if value is None:
            return
        original_name = str(name)
        safe_name = HDF5Database._safe_name(original_name)

        if safe_name in group:
            del group[safe_name]

        dataset = group.create_dataset(safe_name, data=value)
        dataset.attrs["original_name"] = original_name

    def save_shot(self, shot: Shot) -> None:
        """Save one Shot object in the hierarchical structure."""

        with h5py.File(self.filename, "a") as h5file:

            shot_name = f"{int(shot.shot_number):06d}"

            # Create or replace shot group
            shots_group = h5file.require_group("shots")

            if shot_name in shots_group:
                del shots_group[shot_name]

            shot_group = shots_group.create_group(shot_name)

            # -------------------------------------------------
            #                       Metadata
            # -------------------------------------------------
            metadata = shot_group.create_group("metadata")
            metadata.attrs["shot_number"] = int(shot.shot_number)
            metadata.attrs["moving"] = bool(shot.moving)

            # -------------------------------------------------
            #                       Actuators
            # -------------------------------------------------
            actuators_group = shot_group.create_group("actuators")

            for actuator in shot.actuators.values():

                for motor in actuator.get("motors", {}).values():

                    motor_name = motor.get("name")
                    position = motor.get("position")

                    if motor_name is not None:
                        self._write_value(
                            actuators_group,
                            motor_name,
                            position
                        )

            # -------------------------------------------------
            #                       Diagnostics
            # -------------------------------------------------
            diagnostics_group = shot_group.create_group("diagnostics")

            for diagnostic in shot.diagnostics.values():

                diag_name = diagnostic.get("name", "unknown")

                diag_group = diagnostics_group.create_group(
                    self._safe_name(diag_name)
                )

                diag_group.attrs["original_name"] = diag_name

                for variable_name, value in diagnostic.get(
                    "plottables", {}
                ).items():

                    if isinstance(value, (int, float, np.number)):
                        self._write_value(
                            diag_group,
                            variable_name,
                            value
                        )

    def save_summary(self, dataframe: pd.DataFrame) -> None:
        """Save the complete DataFrame as one dataset per column."""

        with h5py.File(self.filename, "a") as h5file:

            if "summary" in h5file:
                del h5file["summary"]

            summary = h5file.create_group("summary")

            summary.attrs["number_of_shots"] = len(dataframe)

            for column in dataframe.columns:

                values = dataframe[column].to_numpy()
                name = self._safe_name(column)

                # Store strings using variable-length UTF-8
                if values.dtype.kind in ("O", "U", "S"):
                    values = np.array(
                        ["" if pd.isna(v) else str(v) for v in values],
                        dtype=h5py.string_dtype("utf-8")
                    )

                dataset = summary.create_dataset(name, data=values)
                dataset.attrs["original_name"] = str(column)

    def save(self, shot, dataframe: pd.DataFrame) -> None:
        """Save both individual shot and summary table."""

        self.save_shot(shot)
        self.save_summary(dataframe)


