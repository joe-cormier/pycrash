from tabulate import tabulate

# Create Project
class Project:
    """
    """

    def __init__(self):
        self.pname = input("Project Name: ")
        self.pdesc = input("Project Description: ")
        self.sim_type = input("Simulation Type [SV/MV]: ")

        if self.sim_type == "MV":
            self.impact_type = input("Impact Type (SS, IMPC, SDOF): ")

            if (self.impact_type not in ["SS", "IMPC", "SDOF"]):
                print("Not a valid impact type, choose SS, IMPC or SDOF. Value set to SDOF")
                self.impact_type == "SDOF"
        else:
            self.impact_type = "none"

        self.note = input("Note: ")

    def show(self):
        print(tabulate([["Project", "Description", "Impact Type", "Simulation Type", "Note"],
                         [self.pname, self.pdesc, self.impact_type, self.sim_type, self.note]]))

    # TODO: add vehicles to project?
    #def add_vehicles(vehicle_list)

# Create vehicle
class Vehicle:
    """requires 'Name' - used to idenify vehicle in simulations"""

    veh_count = 0
    instances: set # initialize instances
    instances = set()

    @classmethod
    def get_instances(cls):
        return cls.instances

    def __init__(self, name):
        self.name = name
        pass

    def manual_input(self):
        self.year = int(input("Model Year: "))
        self.make = input("Vehicle Make: ")
        self.model = input("Vehicle Model: ")
        self.vin = input("Vehicle VIN: ")
        self.weight = float(input("Vehicle Weight (lb): "))

        # will add 1 to vehicle count if manual entry was sucessful
        Vehicle.veh_count += 1
        Vehicle.instances.add(self)

    # TODO: save data to pick and a csv file
    def

    def get_count(self):
        print(Vehicle.veh_count)

# create vehicle motion
# TODO: add vehicles to planar motion, plot motion for each vehicle added?
class PlanarMotion(vehicle):
    def __init__(self):
        pass
