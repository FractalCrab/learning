import numpy as np

def normalize_data(data):
    mean = np.mean(data)
    std = np.std(data)
    return (data - mean) / std


