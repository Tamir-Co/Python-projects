import numpy as np
import importlib
import time
# VERSION 1.2 #
VERSION = 1.2
######################################################################################################
######################################################################################################
## NOTICE THIS IS A TEST I MADE MYSELF AND NOT THE LECTURERES. GETTING THE SAME/DIFFERENT ANSWER AS/FROM ME DOESNT MEAN
## ANYTHING. I DO NOT TAKE RESPONSABILITY THAT THE ANSWERS HERE ARE CORRECT, YOU ARE SIMPLY COMPARED TO THE RESULTS I
## GOT FROM RUNNING THE TEST.

# Change the file name to your ID number !!!!!
File = 'ex4_tiuta'

## DEBUGGING PARAMETERS ##
# DEBUG MODE, turns on the display map after each iteration
DEBUG_MODE = False
# TEST_FILTER, you can turn tests on and off(replace with False to turn off a test)
TEST_FILTER = [True,  # test1- normal test
               True,  # test2- jumping over test(medium sonar)
               True,  # test3- tight test(narrow sonar)
               True,  # test4- wide sonar(large range)
               True,  # test5- no self.mines found test(wide sonar small range)
               True,  # test6a- check self.mines at start(movement is in the other direction)
               True,  # test6b- fov and self.mines in mid duration
               True,  # test6c- run test after timesteps
               True]  # test7-  checking the set_course function
######################################################################################################
######################################################################################################


####################################################################
class Checker:
    def __init__(self):

        # the results i got from running this simulations
        self.my_fov = [{(11, 12): True, (11, 13): True, (12, 8): True, (12, 9): True, (12, 10): True, (12, 11): True,
                        (12, 12): True, (13, 8): True, (13, 9): True, (13, 10): True, (13, 11): True, (14, 8): True,
                        (14, 9): True, (14, 10): True, (15, 8): True, (15, 9): True, (16, 7): True, (16, 8): True,
                        (17, 7): True},
                       {(18, 14): True, (18, 15): True, (18, 16): True, (18, 17): True, (18, 18): True, (18, 19): True,
                        (18, 20): True, (19, 15): True, (19, 16): True, (19, 17): True, (19, 18): True, (19, 19): True,
                        (19, 20): True, (20, 16): True, (20, 17): True, (20, 18): True, (20, 19): True, (20, 20): True,
                        (21, 17): True, (21, 18): True, (21, 19): True, (21, 20): True, (22, 18): True, (22, 19): True,
                        (22, 20): True, (23, 19): True, (23, 20): True, (24, 20): True},
                       {(1, 1): True, (2, 1): True, (2, 2): True, (2, 3): True, (3, 1): True, (3, 2): True, (3, 3): True,
                        (3, 4): True, (3, 5): True, (4, 1): True, (4, 2): True, (4, 3): True, (4, 4): True, (4, 5): True,
                        (4, 6): True, (4, 7): True, (5, 1): True, (5, 2): True, (5, 3): True, (5, 4): True, (5, 5): True,
                        (6, 1): True, (6, 2): True, (6, 3): True, (7, 1): True},
                       {(6, 7): True, (7, 8): True, (8, 9): True, (9, 10): True, (10, 11): True, (11, 12): True,
                        (12, 12): True, (12, 13): True, (13, 14): True, (14, 15): True, (15, 16): True, (16, 17): True,
                        (17, 18): True},
                       {(10, 10): True},
                       {(9, 21): True, (10, 20): True, (10, 21): True, (11, 19): True, (11, 20): True, (11, 21): True, (12, 18): True, (12, 19): True, (12, 20): True, (12, 21): True, (13, 17): True, (13, 18): True, (13, 19): True, (13, 20): True, (13, 21): True, (14, 16): True, (14, 17): True, (14, 18): True, (14, 19): True, (14, 20): True, (14, 21): True, (15, 15): True, (15, 16): True, (15, 17): True, (15, 18): True, (15, 19): True, (15, 20): True, (15, 21): True, (16, 16): True, (16, 17): True, (16, 18): True, (16, 19): True, (16, 20): True, (16, 21): True, (17, 17): True, (17, 18): True, (17, 19): True, (17, 20): True, (17, 21): True, (18, 18): True, (18, 19): True, (18, 20): True, (18, 21): True, (19, 19): True, (19, 20): True, (19, 21): True, (20, 20): True, (20, 21): True, (21, 21): True},
                       {(9, 8): True, (10, 8): True, (10, 9): True, (11, 8): True, (11, 9): True, (11, 10): True, (12, 8): True, (12, 9): True, (12, 10): True, (12, 11): True, (13, 8): True, (13, 9): True, (13, 10): True, (13, 11): True, (13, 12): True, (14, 8): True, (14, 9): True, (14, 10): True, (14, 11): True, (14, 12): True, (14, 13): True, (15, 8): True, (15, 9): True, (15, 10): True, (15, 11): True, (15, 12): True, (15, 13): True, (15, 14): True, (16, 8): True, (16, 9): True, (16, 10): True, (16, 11): True, (16, 12): True, (16, 13): True, (17, 8): True, (17, 9): True, (17, 10): True, (17, 11): True, (17, 12): True, (18, 8): True, (18, 9): True, (18, 10): True, (18, 11): True, (19, 8): True, (19, 9): True, (19, 10): True, (20, 8): True, (20, 9): True, (21, 8): True},
                       {(5, 12): True, (6, 11): True, (6, 12): True, (7, 10): True, (7, 11): True, (7, 12): True, (8, 9): True, (8, 10): True, (8, 11): True, (8, 12): True, (9, 8): True, (9, 9): True, (9, 10): True, (9, 11): True, (9, 12): True, (10, 7): True, (10, 8): True, (10, 9): True, (10, 10): True, (10, 11): True, (10, 12): True, (11, 6): True, (11, 7): True, (11, 8): True, (11, 9): True, (11, 10): True, (11, 11): True, (11, 12): True, (12, 5): True, (12, 6): True, (12, 7): True, (12, 8): True, (12, 9): True, (12, 10): True, (12, 11): True, (12, 12): True, (13, 4): True, (13, 5): True, (13, 6): True, (13, 7): True, (13, 8): True, (13, 9): True, (13, 10): True, (13, 11): True, (13, 12): True, (14, 3): True, (14, 4): True, (14, 5): True, (14, 6): True, (14, 7): True, (14, 8): True, (14, 9): True, (14, 10): True, (14, 11): True, (14, 12): True},
                       {(12, 13): True, (12, 14): True, (12, 15): True, (13, 10): True, (13, 11): True, (13, 12): True, (13, 13): True, (13, 14): True, (13, 15): True, (14, 13): True, (14, 14): True, (14, 15): True}]
        self.my_mine_list = [[(5, 4), (12, 4), (16, 6), (7, 7), (10, 7), (12, 7), (9, 10), (14, 10)],
                             [(8, 17), (14, 22), (18, 22), (20, 24), (10, 30)],
                             [(3, 1), (6, 3), (4, 6), (3, 8), (1, 12), (2, 12), (5, 14), (7, 15), (6, 16), (2, 17)],
                             [(17, 7), (12, 9), (19, 9), (13, 14), (13, 15), (14, 15), (17, 18)],
                             [],
                             [(12, 20), (16, 20), (20, 20), (9, 21)],
                             [(20, 8), (16, 10), (18, 11), (14, 12), (15, 12), (12, 20), (16, 20), (20, 20), (9, 21)],
                             [(21, 7), (20, 8), (16, 10), (11, 11), (18, 11), (14, 12), (15, 12), (12, 13), (22, 14),
                              (18, 15), (20, 18), (12, 20), (16, 20), (20, 20), (9, 21)],
                             [(11, 4), (8, 6), (15, 6), (16, 7), (12, 8), (14, 12), (12, 14)]]
        # params:
        self.test_names = ["-  regular", "-  skipping", "-  tight", "-  wide sonar", "-  no mines",
                           "a- t=0", "b- mid duration", "c- start after step", "-  set course"]
        self.success_status = [True for i in range(len(self.test_names))]
        self.map_size = [(20, 15), (35, 40), (8, 19), (25, 25), (20, 20), (30, 30), (20, 20)]
        self.mines = [np.zeros(self.map_size[i]).tolist() for i in range(len(self.map_size))]
        self.velocity = [[[0, 1], [1, 1]], [[0, 4], [0, 5], [4, -4]], [[0, 3], [0, -1]],
                         [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]],
                         [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]],
                         [[0, -1], [1, 1], [-1, -1]], [[2, 2]]]
        self.sonar_range = [6, 7, 8, 9, 5, 9, 6]
        self.sonar_angle = [60, 50, 30, 85, 85, 45, 20]
        self.initial_position = [(8, 1), (10, 10), (4, 0), (12, 12), (10, 10), (15, 15), (6, 0)]
        self.duration = [[3, 4], [2, 2, 2], [4, 5], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 3], [3]]

        # test1- normal test
        self.mines[0][5][4] = 1;self.mines[0][8][12] = 1;self.mines[0][10][7] = 1;self.mines[0][7][7] = 1;
        self.mines[0][12][7] = 1;self.mines[0][9][10] = 1;self.mines[0][18][6] = 1;self.mines[0][16][6] = 1;
        self.mines[0][12][4] = 1;self.mines[0][14][10] = 1;self.mines[0][17][11] = 1;

        # test2- skipping test
        self.mines[1][8][17] = 1;self.mines[1][7][19] = 1;self.mines[1][13][19] = 1;self.mines[1][7][25] = 1;self.mines[1][13][23] = 1;
        self.mines[1][14][25] = 1;self.mines[1][13][25] = 1;self.mines[1][16][25] = 1;self.mines[1][12][28] = 1;self.mines[1][12][29] = 1;
        self.mines[1][10][30] = 1;self.mines[1][18][22] = 1;self.mines[1][16][19] = 1;self.mines[1][21][24] = 1;self.mines[1][20][24] = 1;
        self.mines[1][14][22] = 1;

        # test 3- tight test
        self.mines[2][0][9] = 1;self.mines[2][0][6] = 1;self.mines[2][1][12] = 1;self.mines[2][1][7] = 1;self.mines[2][2][12] = 1;
        self.mines[2][2][17] = 1;self.mines[2][3][1] = 1;self.mines[2][3][8] = 1;self.mines[2][4][6] = 1;self.mines[2][5][14] = 1;
        self.mines[2][6][16] = 1;self.mines[2][6][3] = 1;self.mines[2][7][13] = 1;self.mines[2][7][15] = 1;

        # test 4- wide sonar test
        self.mines[3][13][14] = 1;self.mines[3][13][15] = 1;self.mines[3][14][15] = 1;self.mines[3][17][18] = 1;self.mines[3][16][18] = 1;
        self.mines[3][16][16] = 1;self.mines[3][11][16] = 1;self.mines[3][15][14] = 1;self.mines[3][14][13] = 1;self.mines[3][16][11] = 1;
        self.mines[3][20][9] = 1;self.mines[3][10][8] = 1;self.mines[3][8][15] = 1;self.mines[3][17][7] = 1;self.mines[3][12][9] = 1;
        self.mines[3][19][9] = 1;

        # test 5- no self.mines test
        self.mines[4][18][12] = 1;self.mines[4][4][0] = 1;self.mines[4][3][7] = 1;self.mines[4][3][18] = 1;self.mines[4][5][10] = 1;
        self.mines[4][8][10] = 1;self.mines[4][15][18] = 1;self.mines[4][8][13] = 1;self.mines[4][3][7] = 1;self.mines[4][15][7] = 1;
        self.mines[4][2][17] = 1;self.mines[4][2][9] = 1;self.mines[4][2][3] = 1;self.mines[4][0][2] = 1;self.mines[4][3][1] = 1;
        self.mines[4][8][5] = 1;self.mines[4][2][10] = 1;self.mines[4][16][5] = 1;self.mines[4][3][1] = 1;self.mines[4][6][8] = 1;
        self.mines[4][0][11] = 1;self.mines[4][16][0] = 1;

        # test6- 3in1
        self.mines[5][27][10] = 1;self.mines[5][14][12] = 1;self.mines[5][11][11] = 1;self.mines[5][6][22] = 1;
        self.mines[5][2][24] = 1;self.mines[5][15][12] = 1;self.mines[5][6][5] = 1;self.mines[5][9][21] = 1;
        self.mines[5][12][13] = 1;self.mines[5][6][25] = 1;self.mines[5][1][13] = 1;self.mines[5][10][22] = 1;
        self.mines[5][17][28] = 1;self.mines[5][10][3] = 1;self.mines[5][20][18] = 1;self.mines[5][19][6] = 1;
        self.mines[5][29][22] = 1;self.mines[5][3][9] = 1;self.mines[5][13][2] = 1;self.mines[5][15][23] = 1;
        self.mines[5][20][8] = 1;self.mines[5][16][20] = 1;self.mines[5][1][29] = 1;self.mines[5][16][10] = 1;
        self.mines[5][18][15] = 1;self.mines[5][0][22] = 1;self.mines[5][8][6] = 1;self.mines[5][28][4] = 1;
        self.mines[5][9][4] = 1;self.mines[5][18][11] = 1;self.mines[5][4][2] = 1;self.mines[5][22][14] = 1;
        self.mines[5][5][29] = 1;self.mines[5][15][3] = 1;self.mines[5][1][26] = 1;self.mines[5][5][17] = 1;
        self.mines[5][20][20] = 1;self.mines[5][0][11] = 1;self.mines[5][25][27] = 1;self.mines[5][29][14] = 1;
        self.mines[5][29][5] = 1;self.mines[5][16][28] = 1;self.mines[5][5][9] = 1;self.mines[5][11][0] = 1;
        self.mines[5][0][22] = 1;self.mines[5][14][28] = 1;self.mines[5][20][12] = 1;self.mines[5][5][24] = 1;
        self.mines[5][21][7] = 1;self.mines[5][12][20] = 1;

        # test 7- setting course
        self.mines[6][17][4] = 1;self.mines[6][5][8] = 1;self.mines[6][15][3] = 1;self.mines[6][12][14] = 1;
        self.mines[6][15][6] = 1;self.mines[6][8][6] = 1;self.mines[6][12][16] = 1;self.mines[6][16][16] = 1;
        self.mines[6][9][12] = 1;self.mines[6][15][15] = 1;self.mines[6][11][3] = 1;self.mines[6][11][4] = 1;
        self.mines[6][12][9] = 1;self.mines[6][9][14] = 1;self.mines[6][6][14] = 1;self.mines[6][11][13] = 1;
        self.mines[6][16][17] = 1;self.mines[6][13][17] = 1;self.mines[6][14][12] = 1;self.mines[6][16][7] = 1;
        self.mines[6][14][4] = 1;self.mines[6][3][8] = 1;self.mines[6][17][15] = 1;self.mines[6][9][14] = 1;
        self.mines[6][12][8] = 1;

    def check_parameters(self, your_fov, my_fov, your_mine_list, my_mine_list, test_name, test_number):
        # test if it is the same
        if your_fov != my_fov:
            self.success_status[test_number-1] = False
            print("{}{} test: your fov is different than mine:\n\
                your fov: {}\n\
                my fov:   {}".format(test_number, test_name, your_fov, my_fov))
        if your_mine_list != my_mine_list:
            self.success_status[test_number-1] = False
            print("{}{} test: your mine list is different than mine:\n\
                your mine list: {}\n\
                my mine list:   {}".format(test_number, test_name, your_mine_list, my_mine_list))

        if self.success_status[test_number-1]:
            # print("{}{} test: {}".format(test_number, test_name, "\t\t\tPASSED"))
            print(str(test_number) + test_name, "test:\n" + "\t"*5 + "PASSED\n")
        else:
            print(str(test_number) + test_name, "test: Failed")

    def run_tests(self):
        if not File.isdigit():
            print("file name should be a valid id made from only digits")
        if len(File) != 9:
            print("file name should be a valid id made from nine digits")
        # import the py file:
        Module = importlib.import_module(File)

        start = time.process_time()
        first_five_tests = TEST_FILTER[:5]
        for i, test_is_active in enumerate(first_five_tests):
            if test_is_active:
                submarine = Module.HydroCamel(self.sonar_range[i], self.sonar_angle[i], self.map_size[i],
                                              self.initial_position[i], self.velocity[i], self.duration[i],
                                              self.mines[i])

                # on debug mode the test runs using time step until it finishes displaying the map after every time_step
                if DEBUG_MODE:
                    total_number_of_iterations = sum(self.duration[i])
                    submarine.display_map()
                    for j in range(total_number_of_iterations):
                        submarine.time_step()
                        submarine.display_map()
                else:
                    submarine.start()

                # the results you got from running this simulation
                your_fov = submarine.get_sonar_fov()
                your_mine_list = submarine.get_mines()
                self.check_parameters(your_fov, self.my_fov[i],
                                      your_mine_list, self.my_mine_list[i],
                                      self.test_names[i], i+1)

        # the sixth test!
        submarine = Module.HydroCamel(self.sonar_range[5], self.sonar_angle[5], self.map_size[5],
                                      self.initial_position[5], self.velocity[5], self.duration[5], self.mines[5])

        # check what the fov is viewing on time 0
        if TEST_FILTER[5]:
            if DEBUG_MODE:
                submarine.display_map()
            submarine.display_map()
            your_fov = submarine.get_sonar_fov()
            your_mine_list = submarine.get_mines()
            self.check_parameters(your_fov, self.my_fov[5], your_mine_list, self.my_mine_list[5], self.test_names[5], 6)

        # 6b- run one time step and check again everything is fine
        if TEST_FILTER[6]:
            submarine.time_step()
            if DEBUG_MODE:
                submarine.display_map()

            your_fov = submarine.get_sonar_fov()
            your_mine_list = submarine.get_mines()
            self.check_parameters(your_fov, self.my_fov[6], your_mine_list, self.my_mine_list[6], self.test_names[6], 6)

        # 6c test, now we simply let the test run
        if TEST_FILTER[7]:
            submarine.start()
            if DEBUG_MODE:
                submarine.display_map()
            your_fov = submarine.get_sonar_fov()
            your_mine_list = submarine.get_mines()
            self.check_parameters(your_fov, self.my_fov[7], your_mine_list, self.my_mine_list[7], self.test_names[7], 6)

        # test 7: checking that set course works properly
        if TEST_FILTER[8]:
            submarine = Module.HydroCamel(self.sonar_range[6], self.sonar_angle[6], self.map_size[6],
                                          self.initial_position[6], self.velocity[6], self.duration[6], self.mines[6])
            added_duration = [2]
            added_velocity = [[-1, 0]]
            submarine.set_course(added_velocity, added_duration)
            # on debug mode the test runs using time step until it finishes displaying the map after every time_step
            if DEBUG_MODE:
                total_number_of_iterations = sum(self.duration[6])+added_duration[0]
                submarine.display_map()
                for j in range(total_number_of_iterations):
                    submarine.time_step()
                    submarine.display_map()
            else:
                submarine.start()

            added_duration = [1, 2]
            added_velocity = [[3, 0], [0, 2]]
            submarine.set_course(added_velocity, added_duration)
            # on debug mode the test runs using time step until it finishes displaying the map after every time_step
            if DEBUG_MODE:
                total_number_of_iterations = sum(added_duration)
                submarine.display_map()
                for j in range(total_number_of_iterations):
                    submarine.time_step()
                    submarine.display_map()
            else:
                submarine.start()
            your_fov = submarine.get_sonar_fov()
            your_mine_list = submarine.get_mines()
            self.check_parameters(your_fov, self.my_fov[8], your_mine_list, self.my_mine_list[8], self.test_names[8], 7)

        end = time.process_time()
        print("-------V{}-------".format(VERSION))
        check_success = all(self.success_status[i] or not TEST_FILTER[i] for i,v in enumerate(TEST_FILTER))
        if check_success:
            print("Final verdict: Success")
        else:
            print("Final verdict: Fail")

        print("total run time is:", end - start, "seconds")
        if (end-start) > 60*20:
            print("your test took too long! run time should be less than 20 min!")


if __name__ == "__main__":
    checker_obj = Checker()
    checker_obj.run_tests()
