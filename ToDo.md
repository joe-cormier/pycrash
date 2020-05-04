To Do List
=============================

Integrate with GitHub project

Create project input function - generate dictionary for inputs.  


## Project Type
1. Single vehicle motion
2. Impact simulation (with or without pre and post vehicle travel)

## Impact Models
+ SDOF model (effective stiffness)
+ SDOF model (effective stiffness | overlap)
+ planar impulse momentum
+ sideswipe (point-edge interaction, long duration)

## Single Vehicle Motion
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
- Kineticorp data
- HVE simulations

## Impact Simulation
- create categorical values for impact simulation types (SV, SDOF, SDOF_Width, Sideswipe, IMPC)
- use impact plane for all types - defines point of impact and force vector?
- create function to vary impact plane location / angle
- import current terrain descriptors

## Impact Models
### SDOF Model (effective stiffness)
- is force only applied through CG?
- colinear impacts
- effective stiffness
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
