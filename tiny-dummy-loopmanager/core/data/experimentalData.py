from .shot import Shot

from laplace_log import log

class ExperimentalData:
    def __init__(self):
        self.shots = dict({})

    def add_shot(self, master_raw_data: dict) -> None:

        this_shot = Shot.from_master_data(master_data=master_raw_data)
        print(f'This shot: {this_shot}')


    def plot(self, plot_config: dict)->dict:
        pass

    def save_all_data(self)-> None:
        pass

