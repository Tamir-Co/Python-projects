import numpy as np
import matplotlib.pyplot as plot


class HydroCamel:
    def __init__(self, _sonar_range, _sonar_angle, _map_size, _initial_position, _velocity, _duration, _mines_map):
        """ init method for class Auv.
        Input:
        _sonar_range - An integer with values between 3-9, denote the range of the sonar
        _sonar_angle - An integer with values between 15-85 in degrees, denote half of the field of view angle
        _map_size - a tuple (Height, Width) of the map
        _initial_position - a tuple (Py, Px). The starting point of the AUV.
        _velocity - a tuple of lists. each donates a velocity ([Vy1, Vx1], [Vy2, Vx2]...)
        _duration - a list of integers. each denote the time to run the simulation
                                         with the matching velocity [t1, t2,...]
        _mines_map - a list of lists holding the location of all the mines.
        Output None.
        """
        self.sonar_range = _sonar_range
        self.sonar_angle = _sonar_angle / 180 * np.pi  # in radians
        self.map_size = _map_size
        self.position = np.array(_initial_position)
        self.velocities = [(0, 0)] + _velocity
        self.durations = [1] + _duration
        self.mines_array = np.where(np.array(_mines_map) == 1)
        self.mines_array = np.swapaxes(self.mines_array, 0, 1)

        self.is_first_step = True
        self.is_same_velocity = False
        self.fov_coordinates = np.array([])
        self.fov_map = None
        self.head_degree = 0
        self.found_mines = list()
        self.map = np.zeros(_map_size, dtype=int)
        self.map[_initial_position] = 1
        self.update_the_fov()
        self.time_step()
        self.map += self.fov_map

    def get_mines(self):
        """ Returns the position of all the mines that the AUV has found.
        Input None.
        Output A list of tuples. Each tuple holds the coordinates (Yi , Xi) of found mines.
               The list should be sorted.
        """
        return self.found_mines

    def update_the_fov(self):
        """ finds all the current (Yi , Xi) coordinates of the map which are in range for the sonar.
        Input & Output None.
        """
        self.fov_map = np.zeros(self.map_size, dtype=int)
        if self.is_same_velocity:
            self.fov_coordinates += self.velocities[0]
            for (y, x) in self.fov_coordinates:
                self.fov_map[y][x] = 2
        else:
            if not self.is_first_step:
                self.get_heading()

            r = self.sonar_range
            By = -r * np.sin(self.head_degree + self.sonar_angle)
            Bx = r * np.cos(self.head_degree + self.sonar_angle)
            Cy = -r * np.sin(self.head_degree - self.sonar_angle)
            Cx = r * np.cos(self.head_degree - self.sonar_angle)

            norm = By * Cx - Bx * Cy
            fov_array = np.array([[0, 0]])

            for y in range(-r, r+1):
                for x in range(-r, r+1):
                    w1 = np.around((y * Cx - x * Cy) / norm, decimals=15)
                    w2 = np.around((x * By - y * Bx) / norm, decimals=15)
                    if (0 <= w1) and (0 <= w2) and (w1 + w2 <= 1):
                        if x == y == 0:
                            fov_array = np.delete(fov_array, 0, axis=0)
                        fov_array = np.append(fov_array, [[y, x]], axis=0)
                        self.fov_map[y+self.position[0]][x+self.position[1]] = 2
            self.fov_coordinates = fov_array + self.position

    def get_sonar_fov(self):
        """ Returns all the current (Yi , Xi) coordinates of the map which are in range for the sonar.
        Input None.
        Output A dictionary. The keys of the dictionary are tuples of the (Yi , Xi) coordinates
        and the value should be Boolean True
        """
        return {(val[0], val[1]): True for val in self.fov_coordinates}

    def display_map(self):
        """ Display the current map.
        Input & Output None.
        """
        pass
        # im = plot.imshow(self.map)
        # # plot.show()
        # plot.ion()
        # im.set_data(self.map)
        # plot.pause(0.1)

    def get_heading(self):
        """ Returns the Direction of movement of the AUV in Degrees. The heading will be between 0-360.
                    With respect to the x and y axes of the map.
        Input None.
        Output the Direction of movement of the AUV in Degrees.
        """
        if self.velocities:
            self.head_degree = np.arctan2(-self.velocities[0][0], self.velocities[0][1])  # in radians
        degree = -int(self.head_degree * 180 / np.pi)
        return degree if degree >= 0 else degree + 360  # in degrees

    def set_course(self, _velocity, _duration):
        """ Receive new values for the velocity and duration properties.
            Append the new values to the current ones
        Input : Velocity as list of lists.
                Duration as list of integers
        Output None.
        """
        self.velocities += _velocity
        self.durations += _duration

    def insert_mine_to_list(self, new_mine):
        """ Inserts the mine that has just been found to the list and keeps it sorted.
        Input - tuple - The coordinates (y, x) of the mine.
        Output None
        """
        idx = 0
        if self.found_mines:  # if the list is not empty
            for y, x in self.found_mines:
                if new_mine[1] < x:
                    break
                elif new_mine[1] == x:
                    if new_mine[0] <= y:
                        break
                idx += 1
        self.found_mines.insert(idx, new_mine)

    def time_step(self):
        """ Propagate the simulation by one step (one second) if duration > 0
        Input & Output None.
        """
        if self.durations:
            if self.is_first_step:
                self.is_first_step = False
            else:
                self.map -= self.fov_map
                self.map[self.position[0]][self.position[1]] -= 1
                self.position += list(self.velocities[0])
                self.map[self.position[0]][self.position[1]] += 1
                self.update_the_fov()
                self.map += self.fov_map

            self.durations[0] -= 1

            fov = self.get_sonar_fov()  # a dict
            mine_idx = -1
            for mine in self.mines_array:
                mine_idx += 1
                mine = tuple(mine)
                is_in = fov.pop(mine, False)
                if is_in:  # is the mine in the fov
                    self.mines_array = np.delete(self.mines_array, mine_idx, axis=0)
                    self.insert_mine_to_list(mine)
                    self.map[mine] += 1
                    mine_idx -= 1

            if self.durations[0] == 0:
                self.durations.pop(0)
                self.velocities.pop(0)
                self.is_same_velocity = False
            else:
                self.is_same_velocity = True

    def start(self):
        """ Activate the simulation and run until duration has ended
        Input & Output None.
        """
        while self.durations:  # run until the duration is over
            self.time_step()


if __name__ == "__main__":
    pass
