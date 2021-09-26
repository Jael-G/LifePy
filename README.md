# LifePy

## Installation

Install via pip:

    python -m pip install lifepy



## Tutorial on how to use the lifepy

Generate a simulation of size `m*n`. In this example, a 10x10 simulation will be generated, using a random array for the initial position of live and dead cells.

```python
from lifepy import lifepy
simulator = lifepy.Simulator(m_size=10, n_size=10, mode='ASCII')
simulator.generate_array()
```

The `mode` argument determines how to show the simulation. Default mode uses `DEFAULT`, where live cells are shown as white blocks and dead cells are black blocks, for this mode, ANSI escape sequences are used. The other available mode is `ASCII`, where live cells are show as `#` and dead cells as `-`.

You can see the current simulation by using the `show_simulation` method:

```python
simulator.show_simulation()
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

The simulation can procced in two ways.

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

The `printout` method prints the simulation after the step, when set to `True`. By default, it's value is `False`.

#### Continuous simulation

The `continuous_simulation` method does the `step` method until a `KeyboardInterrupt` exception occurs, or until all life in the simulation has ended.

```python
from lifepy import lifepy
simulator2 = lifepy.Simulator(m_size=10, n_size=10, mode='DEFAULT')
simulator2.generate_array()
print("Starting simulation...")
simulator2.continous_simulation(step_deyal=1,printout=True)

```

Output:
```
TO-DO: ADD GIF OF SIMULATION RUNNING
```

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
simulator3.show_simulation()
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
- When an array are being used for the simulation, it will have a 'border' of zeros. This was done for preventing out of index errors when checking for live cells.
Example:

    - ```Original array: [[1,1],[1,1]] -> Array simulated: [[0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0]]```
    
    However, the `get_array` method will NOT return the simulated array, it will return a properly 'cropped' array.

- When using the method `continuous_simulation` with `printout` set to `True`, the module `sys` is used to move the cursor up and delete the line in the terminal m times (m being the amount of columns) by using ```sys.stdout.write("\x1b[1A\x1b[2K")```. This is done because:

    1) It allows to clear the screen without using `os.system('clear')`, which makes the terminal 'blink', making the simulation appear less smooth, as well as having possible security issues.
    2) Works better than using other escape sequences that create empty lines, shifting everything up and therefore making a 'mess'.
    3) Most importantly, it does not deleted nor shifts too far up any previous printed content.
    
    A more efficent way to clear the screen is being looked into, possibly by using the `curses` module.

- Related to the previous point, it is recommended to use m and n values that fit within the screen when printing the simulation. Otherwise, it most likely will appear in an odd way. 