To Do
=============================

### Create issues


### Miscellaneous functions - create class functions
+ load cell barrier data - function
+ create impact pulse - use in impc model or free particle
- generic function for requesting input in loop (when missing needed values)
- dictionary of variables
- default input dictionary contained within kinematics and KinematicsTwo
- create time inputs in these classes, not vehicle class


## Impact Models
+ Impulse Momentum Planar Collision model (Carpenter 2019)
+ create function for running series of impc simulations - plot / table of results
+ download collection of tests, data - create function for processing NHTSA data
+ Sideswipe (point-edge interaction, long duration)
+ SDOF model (effective stiffness) - 90% complete
+ SDOF model (effective stiffness | overlap) - secondary


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

## Impact Models
### SDOF Model (effective stiffness)
- is force only applied through CG?
    - offset value to create moment - use impact plane
- colinear impacts
- braking effects
- if impc provides delta-v, can SDOF predict crush depth if given stiffness and width?



### SDOF Model (effective stiffness | overlap)
- considers the extent that the two vehicles are engaged
- effective stiffness based on width of contact
- oblique / angular impacts

### impc - impulse momentum
- validate
- get outputs - delta-V, energy, slide / no slide
- impact pulse - haversine etc.
- Simon validation - 2004-01-1207  - Day
- RICSAC

### terrain
- how to position vehicle(s) with scene / image
- use black / grey background with plotted white grid?
- terrain is mapped to slope / bank

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
