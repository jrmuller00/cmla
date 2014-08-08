#
# parish object definition file

import math
import sys
import getopt

class cmlaParish(object):
    """
    A class to store parish gym information

    name    parish name

    """

    def __init__(self, *args):
        self.name = ""
        self.teamList = []
        self.teamSchedule = {}
        self.gymSchedule = {}
        return super().__init__(*args)
    




