import curses
import numpy
import random
import sys
import time


class Simulator:
    def __init__(self, m_size=50, n_size=50, mode='DEFAULT', live_char='#', dead_char='-'):
        self.__m_size = m_size
        self.__n_size = n_size
        self.mode = mode
        self.__array = None
        self.live_char = live_char
        self.dead_char = dead_char

    def get_array(self):
        copied_array = self.__array.copy()
        copied_array = numpy.delete(copied_array, 0, 0)
        copied_array = numpy.delete(copied_array, self.__m_size, 0)
        copied_array = numpy.delete(copied_array, 0, 1)
        copied_array = numpy.delete(copied_array, self.__n_size, 1)
        return copied_array.copy()
    

    def get_m_size(self):
        '''
        Returns the size of m (rows)
        '''
        return self.__m_size

    def get_n_size(self):
        '''
        Returns the size of n (columns)
        '''
        return self.__n_size
    
    def __array_not_generated(self):
        return self.__array is None

    def generate_array(self):
        '''
        Generates an array with random living and dead cells

        Generates an array of the specified m*n size, plus the "border"
        Iterates throught the array (without including the border) and sets the value randomly
        to 0 or 1

        Returns 1 if succesfully generated, else returns 0
        '''
        try:
            generated_array = numpy.zeros((self.__m_size + 2, self.__n_size + 2))

            for i in range(1, self.__m_size + 1):
                for j in range(1, self.__n_size + 1):
                    generated_array[i][j] = random.randint(0, 1)

            self.__array = generated_array.copy()
            return 1
        except Exception as e:
            self.__array= None #Added just in case, don't want a partially generated array
            print(e)
            return 0

    def load_array(self, array):
        '''
        Loads a given array
        
        Creates a temporary array to add the empty columns and rows that make the "border",
        then sets self.__array to a copy of the temporary array

        Returns 1 if the array is loaded succesfully, else returns 0
        '''
        if array.shape == (self.__m_size, self.__n_size):
            temp_array = numpy.zeros((1, self.__n_size + 2))

            for row in array:
                new_row = [0.] + list(row) + [0.]
                temp_array = numpy.vstack([temp_array, new_row])

            temp_array = numpy.vstack([temp_array, numpy.zeros((1, self.__n_size + 2))])

            self.__array = temp_array.copy()
            return 1
        else:
            raise Exception("Invalid array size. Expected size: ({}, {}) but {} was given".format(self.__m_size, self.__n_size,
                                                                                        array.shape))
        
        return 0

    def get_simulation(self,printout=False):

        '''
        Returns the string used to represet the array when doing the simulation

        '''

        if self.__array_not_generated():
            raise Exception("Array is NoneType. Array most be generated or loaded.")


        array_string = ''
        for i in range(1, self.__m_size + 1):
            for j in range(1, self.__n_size + 1):

                if self.mode == 'DEFAULT':
                    if self.__array[i][j]:
                        array_string += "\u001b[47m" + " " + "\033[0;0m"
                    else:
                        array_string += "\u001b[00;1m" + " " + "\033[0;0m"
                    
                    array_string += "\033[0;0m"

                elif self.mode == 'ASCII':
                    if self.__array[i][j]:
                        array_string += f"{self.live_char}"
                    else:
                        array_string += f"{self.dead_char}"

            array_string += "\n"

        if printout:
            print(array_string)
        return array_string

    def step(self, printout=False):
        '''
        Advances the simulation 1 step foward. If succesful returns 1. If it's unable to do a step 
        (the simulation has ended), returns 0.
        '''
        if self.__array_not_generated():
            raise Exception("Array is NoneType. Array most be generated or loaded.")


        if not numpy.count_nonzero(self.__array) == 0:
            try:
                copied_array = self.__array.copy()
                final_array = numpy.zeros((self.__m_size + 2, self.__n_size + 2))

                for i in range(1, self.__m_size + 1):
                    for j in range(1, self.__n_size + 1):

                        current_cell = copied_array[i][j]
                        surrounding_cells = [
                            copied_array[i - 1][j - 1], copied_array[i - 1][j], copied_array[i - 1][j + 1],
                            copied_array[i][j - 1], copied_array[i][j + 1],
                            copied_array[i + 1][j - 1], copied_array[i + 1][j], copied_array[i + 1][j + 1]
                        ]

                        alive_surrounding_cells = surrounding_cells.count(True)
                        if (not current_cell and alive_surrounding_cells == 3) or (
                                current_cell and alive_surrounding_cells == 2 or alive_surrounding_cells == 3):
                            final_array[i][j] = True
                        if current_cell and alive_surrounding_cells != 2 and alive_surrounding_cells != 3:
                            final_array[i][j] = False

                        self.__array = final_array.copy()

                if printout:
                    self.get_simulation(printout)
                return 1

            except KeyboardInterrupt:
                self.__array=copied_array.copy()
                raise KeyboardInterrupt

        else:
            print("Cannot do any more steps. All life has ended in the simulation")
            return 0

    def continuous_simulation(self, step_delay=0, printout=False):
        '''
        Show the simulation in a curses window

        Only 'ASCII' mode works.
        '''

        saved_mode = self.mode
        self.mode = 'ASCII'            
        if self.__array_not_generated():
            raise Exception("Array is NoneType. Array most be generated or loaded.")
        
        if printout:
            simulation_screen = curses.initscr()
            simulation_screen.clear()
            
        try:
            while True:
                self.step(False)

                if printout:
                    simulation_screen.clear()
                    try:
                        simulation_screen.addstr(0,0, self.get_simulation(printout=False))
                    except:
                        pass
                    simulation_screen.refresh()

                if numpy.count_nonzero(self.__array) == 0:
                    print("All life has ended in the simulation")
                    break

                time.sleep(step_delay)

        except KeyboardInterrupt:
            if printout:
                simulation_screen.clear()
                curses.nocbreak()
                curses.echo()
                curses.endwin()
                simulation_screen.clear()
            print("Exiting simulation")
        
        self.mode = saved_mode
