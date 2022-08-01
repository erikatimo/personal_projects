"""
    Created at: 2022-03-29
    Author: Erika Timo de Oliveira
    Description: Multiple Linear Regression between Nasdaq Assets 
"""

import numpy as np
import pandas as pd
from datetime import datetime 
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")
import pdb

from plot_functions import *


