"""
class for static impulse momentum model
"""

from .carpenter_momentum_calcs import impc
from .collision_plane import define_impact_plane, define_impact_edge

class IMPC():
    def __init__(name, veh1, veh2, user_sim_defaults = None):
        self.name = name
        self.type = 'impc_carpenter'             # class type for saving files
        self.veh1 = deepcopy(veh1)
        self.veh2 = deepcopy(veh2)

        print(f"Create impact point for {self.veh1.name} = striking vehicle")
        print("")
        self.veh1 = define_impact_plane(veh1)

        print(f"Create impacting edge for {self.veh2.name} = struck vehicle")
        print("")
        self.veh2 = define_impact_edge(veh2, iplane = False)

    # plot initial positions show data on chart
        # load defaults
        if user_sim_defaults:
            # TODO: create check for user sim_defaults_input
            self.sim_defaults = user_sim_defaults
        else:
            self.sim_defaults = {'vehicle_mu':0.3,
                                 'cor':0.2}
