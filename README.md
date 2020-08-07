Pycrash
------------------------------------------------

Pycrash is a 2D mathematical model for simulating vehicle motion and vehicular impacts using a variety of approaches based on fundamental physics and published accident reconstruction techniques.


#### Planar Vehicle Motion
1. Single vehicle motion based on driver inputs (brake, throttle, steer)
2. Multi-vehicle motion with impact detection
  - currently two vehicles, impact response based on two different approaches.

#### Impact Simulation
1. Single Degree of Freedom Model
  - basic 2D collision with user defined stiffness values and braking effects
  - no pre and post vehicle motion model use for impact severity calculations
  - vehicle specific data is published for most vehicles by the [National Highway Traffic Safety Administration](https://www-nrd.nhtsa.dot.gov/database/veh/veh.htm)
  - use published stiffness data such as [Bonugli et al.](https://www.sae.org/publications/technical-papers/content/2017-01-1417/) or [Lee et al.](https://www.sae.org/publications/technical-papers/content/2014-01-0351/) as examples

2. Sideswipe
    - similar to previous model developed and validated by [Funk et al.](https://www.sae.org/publications/technical-papers/content/2004-01-1185/)
    - improved to allow for driver inputs and flexible approach angles and contact locations
3. Impulse Momentum Planar Collision
  - model based on conservation of momentum incorporating inter-vehicular sliding developed by [Carpenter et al.](https://www.sae.org/publications/technical-papers/content/2019-01-0422/)


#### Validation
  - Single vehicle motion
    - physical testing
    - side by side with other reconstruction software
  - Sideswipe
  - Momentum
  - validation data available in this repo

#### Modular Design

  - Model calculations divided into modules to allow for future improvements
  - Vehicle motion incorporates a modular linear tire model to determine slip condition based on weight shift from longitudinal and lateral acceleration. 


### Recommendations
- If you are new to python, I recommend looking into [Anaconda](https://www.anaconda.com/) it is an easy way to get python working on your machine.
- Pycrash is built around [Pandas](https://pandas.pydata.org/) so you can manipulate the output of Pycrash functions directly with Pandas.
- See [Github](https://github.com/joe-cormier/pycrash) repo for tutorials, Jupyter Notebooks and validation data
