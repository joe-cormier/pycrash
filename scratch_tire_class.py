class Tire:
    """
    create instance of a tire
    define location of tire, tire properties which will determine
    how forces are calculated
    """
    def __init__(self, name, alpha_max=0.174533, mu_max=0.8, input_dict=None):
        self.name = str(name)
        self.type = "tire"
        self.alpha_max = alpha_max * mu_max
        self.mu_max = mu_max

        if input_dict is not None:
            for key, value in input_dict.items():
                if key in ['rx', 'ry', 'percent_disabled', 'time_disabled']:
                    setattr(self, key, float(value))
                elif key in ['steer', 'drive']:
                    setattr(self, key, bool(value))
                else:
                    print(f"Input entry {key} unknown, setting to {value}")
                    setattr(self, key, float(value))

            print(f'Tire inputs for {self.name} applied successfully')