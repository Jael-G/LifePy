import numpy
import random
import sys
import time


class Simulator:
    def __init__(self, m_size=50, n_size=50, mode='DEFAULT'):
        self.__m_size = m_size
        self.__n_size = n_size
        self.mode = mode
        self.__array = None

    def get_array(self):
        copied_array = self.__array.copy()
        copied_array = numpy.delete(copied_array, 0, 0)
        copied_array = numpy.delete(copied_array, self.__m_size, 0)
        copied_array = numpy.delete(copied_array, 0, 1)
        copied_array = numpy.delete(copied_array, self.__n_size, 1)
        return copied_array.copy()

    def get_m_size(self):
        return self.__m_size

    def get_n_size(self):
        return self.__n_size

    def generate_array(self):
        generated_array = numpy.zeros((self.__m_size + 2, self.__n_size + 2))

        for i in range(1, self.__m_size + 1):
            for j in range(1, self.__n_size + 1):
                generated_array[i][j] = random.randint(0, 1)

        self.__array = generated_array.copy()

    def load_array(self, array):
        if array.shape == (self.__m_size, self.__n_size):
            temp_array = numpy.zeros((1, self.__n_size + 2))

            for row in array:
                new_row = [0.] + list(row) + [0.]
                temp_array = numpy.vstack([temp_array, new_row])

            temp_array = numpy.vstack([temp_array, numpy.zeros((1, self.__n_size + 2))])

            self.__array = temp_array.copy()
        else:
            print("Invalid array size. Expected size: ({}, {}) but {} was given".format(self.__m_size, self.__n_size,
                                                                                        array.shape))

    def show_simulation(self):
        array_string = ''
        for i in range(1, self.__m_size + 1):
            for j in range(1, self.__n_size + 1):

                if self.mode == 'DEFAULT':
                    if self.__array[i][j]:
                        array_string += "\u001b[47m" + " "
                    else:
                        array_string += "\u001b[00;1m" + " "

                elif self.mode == 'ASCII':
                    if self.__array[i][j]:
                        array_string += "#"
                    else:
                        array_string += "-"

            array_string += "\n"
            array_string += "\033[0;0m"

        print(array_string)

    def step(self, printout=False):
        if not numpy.count_nonzero(self.__array) == 0:

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
                self.show_simulation()
        else:
            print("Cannot do any more steps. All life has ended in the simulation")

    def continuous_simulation(self, step_delay=0, printout=False):
        try:
            while True:
                self.step(printout)

                if numpy.count_nonzero(self.__array) == 0:
                    print("All life has ended in the simulation")
                    break

                time.sleep(step_delay)

                if printout:
                    for _ in range(self.__m_size + 1):
                        sys.stdout.write("\x1b[1A\x1b[2K")

        except KeyboardInterrupt:
            print("Exiting simulation")
