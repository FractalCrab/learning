import numpy as np
from abc import ABC, abstractmethod

def normalize_data(data):
    mean = np.mean(data)
    std = np.std(data)
    return (data - mean) / std


def mean_squared_error(y_true, y_pred):

        assert len(y_true) == len(y_pred), "Input arrays must have the same length."
        return np.mean((y_true - y_pred) ** 2)

def root_mean_squared_error(y_true, y_pred):
        assert len(y_true) == len(y_pred), "Input arrays must have the same length."
        mse = np.mean((y_true - y_pred) ** 2)
        return np.sqrt(mse)

def r2_score(y_true, y_pred):
        assert len(y_true) == len(y_pred), "Input arrays must have the same length."
        mean_y = np.mean(y_true)
        ss_total = np.sum((y_true - mean_y) ** 2)
        ss_residual = np.sum((y_true - y_pred) ** 2)
        return  1 - (ss_residual / ss_total)


class Model(ABC):
    @abstractmethod
    def loss():
        pass
    @abstractmethod
    def fit():
        pass

    @abstractmethod
    def predict():
        pass

