

def format_plottable_data_dict(data: dict):
    plottables = {}

    for address, address_dictionary in data.items():
        name = address_dictionary['name']
        if type(address_dictionary) is not dict:
            raise ValueError(f'Wrong data dictionary format')

        for key, value in address_dictionary['data'].items():
            if type(value) is float:
                plottables[key] = value

    return address, name, plottables



if __name__ == "__main__":
    dictionary =  {'tcp://147.250.140.85:5556': 
                   {'name': 'dummy_camera', 'data': 
                    {'shot_number': 8, 'motor': [0.0, 0.0], 'electron_charge': 1.0028798580169678, 'electron_energy_mean': 0.9999077916145325, 'time': '16:39:20'}}}
    print(f'Plottables: {format_plottable_data_dict(dictionary)}')
