To Do
=============================

Integrate with GitHub project
Add raise errors

### Miscellaneous functions - create class functions
+ load cell barrier data
+ create impact pulse - use in impc model or free particle

## Impact Models
+ SDOF model (effective stiffness) - 90% complete
+ SDOF model (effective stiffness | overlap) - secondary
+ Impulse Momentum Planar Collision model (Carpenter 2019)
+ Sideswipe (point-edge interaction, long duration)

##  Vehicle Motion
- allow single vehicle model to accept external force

#### Terrain
- boundaries for surface friction / grade / bank
- defined in model plane
- function to provide data to vehicle model as a function of global coordinates (X,Y)

#### Suspension
- simulate body roll and pitch
- adjustable based on reasonable inputs

#### Tire Model
- modular
- friction circle
- maximum side slip
- incorporate tire model in impact simulation

#### Validation
- Vehicle motion
- Impact model

## Impact Simulation
- create categorical values for impact simulation types (SV, SDOF, SDOF_Width, Sideswipe, IMPC)
- use impact plane for all types - defines point of impact and force vector?
- create function to vary impact plane location / angle
- import current terrain descriptors

## Impact Models
### SDOF Model (effective stiffness)
- is force only applied through CG?
    - offset value to create moment - use impact plane
- colinear impacts
- braking effects

### SDOF Model (effective stiffness | overlap)
- considers the extent that the two vehicles are engaged
- effective stiffness based on width of contact
- oblique / angular impacts

## Validation
- narrow offset tests
- 214 tests
- NHTSA v2v impacts

### Planar Impulse Momentum
- Carpenter SAE #

## Validation


### Sideswipe Model
- Funk SAE #


## Validation


## Visualization
- add input to x, y, heading angle for vehicle simulations to update initial position in notebook
