# -----------------------------------------------------------
# sorts a list of hexColors by simulatiry to a target hexColor
# and displays simularity values
#
# File created by Bradley McInerney 30/11/2020
# Email: bradleymcinerney@hotmail.com
# -----------------------------------------------------------

from math import sqrt
from os import path
import sys

# ------------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------
project_colors = ["000000", "ffffff", "7f7f7f"]
target_color_list = project_colors

# ------------------------------------------------------------------------------
# Notes
# ------------------------------------------------------------------------------
# #666666 in ios has an alpha of 0.5 in the project.
# project_colors_ios last updated on 30/11/2020

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------
class ScoreableColor:
	color = None
	score = None

	def __init__(self, color, score):
		self.color = color
		self.score = score

	def __lt__(self, other):
		return self.score < other.score

	def __str__(self):
		return "#" + str(self.color) + ": " + "{:.1f}".format(self.score)

class ScoreableColorList:
        color_list = None

        def __init__(self, color_list):
                self.color_list = color_list

        def __str__(self):
                output = ""
                for col in self.color_list:
                        output += str(col) + "\n"
                return output[:-1]

        def sort(self, reversed=False):
                self.color_list.sort(reverse=reversed)


class ColorScorer:
        @staticmethod
        def hexToRgb(h):
                return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        @staticmethod
        def colorDistance(h1, h2):
                rgb1 = ColorScorer.hexToRgb(h1)
                rgb2 = ColorScorer.hexToRgb(h2)

                rmean = int((rgb1[0] + rgb2[0])/2)
                r = abs(rgb1[0] - rgb2[0])
                g = abs(rgb1[1] - rgb2[1])
                b = abs(rgb1[2] - rgb2[2])
                return sqrt((((512+rmean)*r*r)>>8) + 4*g*g + (((767-rmean)*b*b)>>8))

        @staticmethod
        def scoreColors(target_color, color_list):
                scored_colors = []
                for col in color_list:
                        scored_colors.append(ScoreableColor(col, ColorScorer.colorDistance(target_color, col)))
                return ScoreableColorList(scored_colors)

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
def main():
        # Variables
        reverse = True
        target_color = None
        args = sys.argv
        usage = "Usage: " + args[0] + " hexColor [-r]"
        most_similar = "bottom"
        
        # Handle args
        if len(args) > 1:
                target_color = args[1].lstrip('#')
                
                if '-r' in args:
                        reverse = False
                        most_similar = "top"
        else:
                print("ERROR: invalid arguments\n" + usage)
                return

        # Handle arg errors
        try:
                tc = int(target_color, 16)
                if tc < 0 or tc > 16777215 or len(target_color) != 6:
                        raise ValueError()
        except ValueError:
                print("ERROR: invalid hexColor\n" + usage)
                return

        # Calculate
        colors = ColorScorer.scoreColors(target_color, target_color_list)
        colors.sort(reverse)

        # Print                
        print("------------------------------")
        print(colors)
        print("(Most similar at " + most_similar + ")\n")

if __name__ == "__main__":
        main()
