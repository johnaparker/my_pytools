"""Functions related to index notation, einsum, and tensors"""
import numpy as np

# Levi-Civita symbol
def levi_civita():
    """return the levi-civita symbol"""

    eijk = np.zeros((3, 3, 3))
    eijk[0, 1, 2] = eijk[1, 2, 0] = eijk[2, 0, 1] = 1
    eijk[0, 2, 1] = eijk[2, 1, 0] = eijk[1, 0, 2] = -1
    return eijk
