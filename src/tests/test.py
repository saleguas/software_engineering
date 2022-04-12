import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "tests"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "custom_equation_solver"))
from StaticFunctions import *
from SimplePower import SimplePower
from Multiply import Multiply
from Add import Add
import pytest


print(standardize_linear_format(Multiply(factors=5)).to_string())