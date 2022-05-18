import numpy as np
import matplotlib as mpl
import astropy
from pathlib import Path

def bmp2fits(directory, **kwargs):
    path = Path(directory)
    files = path.rglob(".bmp")

    

    return