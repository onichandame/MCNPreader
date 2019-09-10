# MCNP reader

# Author
Xiao Zhang

# License
no restriction

# Design
The motivation comes from the comparison between 2 MCNP inputs with the same lattice structure but different lattice orientation. The results were entirely different but the cause was not trivial. Therefore I decided to make a program to help compare these 2 inputs. As the development goes on, more features come to my mind. if anything in the roadmap attracts your attention, welcome to contribute based on the latest master commit.

# Roadmap
- Visualize the input geometry in 3D space with a fly-through camera, ideally with a planar cut
- Compare 2 inputs regardless of the indices and the choice of coordinates
- Visualize the output matrix together with the input geometry

## Core
The program must be able to handle certain core functions in order to achieve high level tasks.
- Read input/output: input.py
- Log: logger.py
