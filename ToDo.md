To Do
=============================

### Create issues


### Miscellaneous functions - create class functions
+ create impact pulse - use in impc model or free particle
- generic function for requesting input in loop (when missing needed values)
- dictionary of variables - needs updating

## Impact Models
+ Sideswipe (point-edge interaction, long duration)
+ allow for multiple impacts

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

### impc - impulse momendstum
- RICSAC tests?

### terrain
- how to position vehicle(s) with scene / image
- use black / grey background with plotted white grid?
- terrain is mapped to slope / bank

## Validation
- narrow offset tests
- 214 tests
- NHTSA v2v impacts

