To Do
=============================

Integrate with GitHub project  
Add raise errors  
Create project input function - generate dictionary for inputs.

### Saving Data
+ create new folder for each project (input / reports)

### Miscellaneous functions
+ how to include?

### Classes
+ add plot functions - arguments for changing color / size etc.
  - save plots using project name - "reports directory"
+ subplots for model results (fdx, v, a) - SDOF model
+ record delta-v as a vehicle attribute
+ vehicle - automatically search for vehicle inputs?

### Parametric
+ function for multiple plots - plot_runs(run1, run2, run3, etc.)

## Project Type
1. Single vehicle motion
2. Impact simulation (with or without pre and post vehicle travel)

## Load cell barrier data
+ functions to process data

## Impact Models
+ SDOF model (effective stiffness)
+ SDOF model (effective stiffness | overlap) - later
+ planar impulse momentum (Carpenter)
+ sideswipe (point-edge interaction, long duration)

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
    - offset value to create moment
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
