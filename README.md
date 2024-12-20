Pycrash
=

Pycrash is a 2D mathematical model for simulating vehicle motion and vehicular impacts using a variety of
approaches based on fundamental physics and published accident reconstruction techniques.  In addition to fundamental
applications, Pycrash has accident reconstruction specific modules for obtaining and processing commonly used data

##### Installation (Requires Python > 3.6)
pip install pycrash
[PyPi](https://pypi.org/project/pycrash/)

#### Planar Vehicle Motion
1. Single vehicle motion based on driver inputs (brake, throttle, steer)
2. Multi-vehicle motion and multiple impacts per vehicle

#### Impact Simulation
##### Single Degree of Freedom Model
  - basic 2D collision with user defined stiffness values and braking effects
  - vehicle specific data is published for most vehicles by the [National Highway Traffic Safety Administration](https://www-nrd.nhtsa.dot.gov/database/veh/veh.htm)
  - use published stiffness data such as [Bonugli et al.](https://www.sae.org/publications/technical-papers/content/2017-01-1417/) or [Lee et al.](https://www.sae.org/publications/technical-papers/content/2014-01-0351/) as examples
##### Impulse Momentum Planar Collision
 - model based on conservation of momentum incorporating inter-vehicular sliding developed by [Carpenter et al.](https://www.sae.org/publications/technical-papers/content/2019-01-0422/)
##### Sideswipe (*in progress*)
   - similar to previous model developed and validated by [Funk et al.](https://www.sae.org/publications/technical-papers/content/2004-01-1185/)
   - improved to allow for driver inputs and flexible approach angles and contact locations

#### Validation
  - validation data are provided within the [Github](https://github.com/joe-cormier/pycrash) repo
  - Initial publication in [2021 SAE](https://www.sae.org/publications/technical-papers/content/2021-01-0896/)

#### Modular Design
  - Model calculations divided into modules to allow for future improvements
  - Vehicle motion incorporates a modular linear tire model to determine slip condition based on weight shift from longitudinal and lateral acceleration.

### Collaboration
  - Contributors are welcome - create a branch to develop a new capability or improve the current model
  - There is a list of projects in the report for future applications that I would like to pursue
  - Create an issue if you identify a problem or to make suggestions for future improvements
  - Additional validation data are always welcome

#### Recommendations
- Download Python [here](https://www.python.org/) and install required packages with pip from [PyPi](https://pypi.org/)
- See [Github](https://github.com/joe-cormier/pycrash) repo for tutorials, Jupyter Notebooks and validation data
- The validation and demonstration of Pycrash is best viewed using [Jupyter notebooks](https://jupyter.org/)
