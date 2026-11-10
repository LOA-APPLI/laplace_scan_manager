import h5py
import pandas as pd

def visit_hdf5_items(file: str = "database.h5") -> None:
    with h5py.File(file, "r") as f:

        def print_structure(name, obj):
            print(name, type(obj).__name__)

        f.visititems(print_structure)

def load_hdf5_into_pandas_df(file: str="database.h5") -> pd.DataFrame:
    with h5py.File(file, "r") as f:

        summary = f["summary"]

        data = {}

        for name, dataset in summary.items():

            original_name = dataset.attrs["original_name"]
            data[original_name] = dataset[:]

        dataframe = pd.DataFrame(data)
    return dataframe

if __name__ == "__main__":
    visit_hdf5_items("database.h5")
    dataframe = load_hdf5_into_pandas_df()
    print(f'dataframe: {dataframe}')