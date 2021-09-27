# LifePy

## Installation

Install via pip:

    python -m pip install lifepy



## Tutorial on how to use the lifepy

Generate a simulation of size `m*n`. In this example, a 10x10 simulation will be generated, using a random array for the initial position of live and dead cells.

```python
from lifepy import lifepy
simulator = lifepy.Simulator(m_size=10, n_size=10, mode='ASCII', live_char='#', dead_char='-')
simulator.generate_array()
```

The `mode` argument determines how to show the simulation. By default it is set to `DEFAULT`, where live cells are shown as white blocks and dead cells are black blocks, for this mode, ANSI escape sequences are used. The other available mode is `ASCII`. For `ASCII` the character used for live cells and dead cells can be specified with the `live_char` and `dead_char` accordingly. By default `#` is used for live cells and `-` is used for dead cells.

You can see the current simulation by using the `get_simulation` method:

```python
simulator.get_simulation(printout=True)
```
Output:
```
--#-##-#--
##-#----#-
##-#######
-#-######-
-#--#-#--#
###---##-#
#-####-###
#----#--#-
---###-#-#
-##-##-#--
```
The `get_simulation` method returns the string used to represet the simulation(like the one shown in the output). The `printout` parameter prints the simulation when set to `True` and is used for other methods as well. By default, `printout` is set to `False` in all the methods.

The simulation can advance in two ways.

#### Step by step

The `step` method only moves the simulation foward once. In other words, the simulation does one step.

Using the same simulation as before:
```python
simulation.step(printout=True)
```
Output:
```
-####-----
#--------#
---------#
-#--------
----#----#
#--------#
#-####---#
-##-------
-###---#--
--#--#--#-
```


#### Continuous simulation

The `continuous_simulation` method does the `step` method until a `KeyboardInterrupt` exception occurs, or until all life in the simulation has ended. Since `continuous_simulation` uses the `curses` module it does not support ANSI escape sequences. Therefore, while on `continuous_simulation` the mode is `ASCII`, and after the simulation is interupted or it ends, the mode is set back to its original value.

```python
from lifepy import lifepy
simulator2 = lifepy.Simulator(m_size=30, n_size=50, mode='DEFAULT')
simulator2.generate_array()
simulator2.continuous_simulation(step_deyal=.1,printout=True)

```

Output:

![GIF example of continuous simulation](https://github.com/Jael-G/lifepy/blob/main/output_example.gif)

The `step_delay` determines the time (in seconds) between each step.

### When taking steps
It is important to take into account that the `m*n` size specified at the start is the size of the array, but also the size of the simulation. Therefore, any live cells that 'should' generate but are outside the `m*n` size are never generated.
### Loading an array

Instead of generating a random array for the simulation, a predetermined one can be loaded. However the size of the array must equal the size of the simulation.

```python
from lifepy import lifepy
import numpy

simulator3 = lifepy.Simulator(m_size=10, n_size=10, mode='ASCII')
pre_array = numpy.array([[1,1,1,1,1,1,1,1,1,1],
                        [0,0,0,0,0,0,0,0,0,0],
                        [1,1,1,1,1,1,1,1,1,1],
                        [0,0,0,0,0,0,0,0,0,0],
                        [1,1,1,1,1,1,1,1,1,1],
                        [0,0,0,0,0,0,0,0,0,0],
                        [1,1,1,1,1,1,1,1,1,1],
                        [0,0,0,0,0,0,0,0,0,0],
                        [1,1,1,1,1,1,1,1,1,1],
                        [0,0,0,0,0,0,0,0,0,0]])

simulator3.load_array(pre_array)
simulator3.get_simulation(printout=True)
```

Output:
```
##########
----------
##########
----------
##########
----------
##########
----------
##########
----------
```

#### Get values from the array

The `get_array` method returns a copy of the array being used for the simulation in its current step. For the dimensions of the array, the methods `get_m_size` (for rows) and
`get_n_size` (for columns) will return said dimensions.


#### Notes
- When an array is being used for the simulation, it will have a 'border' of zeros. This was done for preventing out of index errors when checking for live cells.
Example:

    - ```Original array: [[1,1],[1,1]] -> Array simulated: [[0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0]]```
    
    However, the `get_array` method will NOT return the simulated array, it will return a properly 'cropped' array.


- It is recommended to use m and n values that fit within the screen when printing the simulation. Otherwise, it most likely will appear in an odd way. 