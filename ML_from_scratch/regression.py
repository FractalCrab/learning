import numpy as np
import plotly.express as px
class LinearRegression:
    def __init__(self, learning_rate=0.01, n_iters=1000, reg_lambda=0.0):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None
        self.regularization = False
        self.reg_lambda = reg_lambda 

    def set_initial_params(self, n_features):
        self.weights = np.random.rand(n_features) * 0.01
        self.bias = 0

    def forward(self, X):
        return np.dot(X, self.weights) + self.bias

    def loss(self, y_pred, y_true):
        n = len(y_true)
        mse = np.mean((y_pred - y_true) ** 2)
        if not self.regularization:
            return mse
        reg_term = (self.reg_lambda / (2 * n)) * np.sum(self.weights ** 2)
        return mse + reg_term

    def backward(self, y_pred):
        n = len(y_pred)
        dw = (1 / n) * np.dot(self._X.T, (y_pred - self._y))
        db = (1 / n) * np.sum(y_pred - self._y)
        if self.regularization:
            dw += (self.reg_lambda / n) * self.weights
        return dw, db

    def fit(self, X, y, plot_loss=True):
        
        costs = []

        if X.ndim == 1:
            X = X.reshape(-1, 1)

        n_samples, n_features = X.shape
        self.set_initial_params(n_features)

        self._X = X
        self._y = y

        for i in range(self.n_iters):
            y_pred = self.forward(X)
            # print(y_pred)
            loss = self.loss(y_pred, self._y)
            dw, db = self.backward(y_pred)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

            costs.append(loss)

            if i % 100 == 0:
                print(f"Iteration {i}: Loss = {loss}")

            if abs(loss) < 1e-7:
                print(f"Converged at iteration {i}")
                break

        if plot_loss:
            fig = px.line(y=costs, title="Cost vs Iteration", template="plotly_dark")
            fig.update_layout(
                title_font_color="#41BEE9",
                xaxis=dict(color="#41BEE9", title="Iterations"),
                yaxis=dict(color="#41BEE9", title="Cost")
            )

            fig.show()

    def predict(self, X):
        return self.forward(X)

    def save(self, filename):

        np.savez(
            filename,
            weights=self.weights,
            bias=self.bias,
            learning_rate=self.lr,
            n_iters=self.n_iters
        )

    @classmethod
    def load(cls, filename):

        data = np.load(filename)
        model = cls(
            learning_rate=float(data["learning_rate"]),
            n_iters=int(data["n_iters"])
        )
        model.weights = data["weights"]
        model.bias = float(data["bias"])
        return model