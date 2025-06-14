import numpy as np
import matplotlib.pyplot as plt
from typing import List, Callable, Optional

class Variable:
    def __init__(self, data: float, grad: float = 0.0, _children: tuple = (), _op: str = ''):
        self.data = data
        self.grad = grad
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op
    
    def __repr__(self):
        return f"Variable(data={self.data:.4f}, grad={self.grad:.4f})"
    
    def __add__(self, other):
        other = other if isinstance(other, Variable) else Variable(other)
        out = Variable(self.data + other.data, _children=(self, other), _op='+')
        
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        
        return out
    
    def __radd__(self, other):  # For other + self
        return self + other
    
    def __mul__(self, other):
        other = other if isinstance(other, Variable) else Variable(other)
        out = Variable(self.data * other.data, _children=(self, other), _op='*')
        
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        
        return out
    
    def __rmul__(self, other):  # For other * self
        return self * other
    
    def __sub__(self, other):
        return self + (-other)
    
    def __rsub__(self, other): 
        return other + (-self)
    
    def __neg__(self):  # For -self
        return self * -1
    
    def __truediv__(self, other):
        return self * (other ** -1)
    
    def __rtruediv__(self, other):  
        return other * (self ** -1)
    
    def __pow__(self, other):
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Variable(self.data**other, _children=(self,), _op=f'**{other}')
        
        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad
        out._backward = _backward
        
        return out
    
    def relu(self):
        out = Variable(0 if self.data < 0 else self.data, _children=(self,), _op='ReLU')
        
        def _backward():
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward
        
        return out
    
    def tanh(self):
        x = self.data
        t = (np.exp(2*x) - 1)/(np.exp(2*x) + 1)
        out = Variable(t, _children=(self,), _op='tanh')
        
        def _backward():
            self.grad += (1 - t**2) * out.grad
        out._backward = _backward
        
        return out
    
    def backward(self):
        # Topological order all of the children in the graph
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        
        # Go one variable at a time and apply the chain rule to get its gradient
        self.grad = 1
        for v in reversed(topo):
            v._backward()

class NumericalGradient:
    """
    Compute gradients using finite differences for comparison.
    """
    @staticmethod
    def gradient(f: Callable, x: float, h: float = 1e-5) -> float:
        """Compute numerical gradient using central difference."""
        return (f(x + h) - f(x - h)) / (2 * h)
    
    @staticmethod
    def partial_gradient(f: Callable, x: List[float], i: int, h: float = 1e-5) -> float:
        """Compute partial derivative with respect to x[i]."""
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += h
        x_minus[i] -= h
        return (f(x_plus) - f(x_minus)) / (2 * h)

def simple_function_example():
    """Example: f(x) = x^2 + 2x + 1, df/dx = 2x + 2"""
    print("=== Simple Function Example ===")
    print("f(x) = x^2 + 2x + 1")
    print("Analytical derivative: df/dx = 2x + 2")
    
    x_val = 3.0
    
    # Automatic differentiation
    x = Variable(x_val)
    y = x*x + 2*x + 1
    y.backward()
    auto_grad = x.grad
    
    # Numerical differentiation
    f = lambda x: x**2 + 2*x + 1
    numerical_grad = NumericalGradient.gradient(f, x_val)
    
    # Analytical result
    analytical_grad = 2*x_val + 2
    
    print(f"At x = {x_val}:")
    print(f"  Automatic gradient: {auto_grad:.6f}")
    print(f"  Numerical gradient: {numerical_grad:.6f}")
    print(f"  Analytical gradient: {analytical_grad:.6f}")
    print()

def complex_function_example():
    """Example with composition: f(x) = tanh(x^2 + 2x)"""
    print("=== Complex Function Example ===")
    print("f(x) = tanh(x^2 + 2x)")
    
    x_val = 1.5
    
    # Automatic differentiation
    x = Variable(x_val)
    y = (x*x + 2*x).tanh()
    y.backward()
    auto_grad = x.grad
    
    # Numerical differentiation
    f = lambda x: np.tanh(x**2 + 2*x)
    numerical_grad = NumericalGradient.gradient(f, x_val)
    
    print(f"At x = {x_val}:")
    print(f"  Automatic gradient: {auto_grad:.6f}")
    print(f"  Numerical gradient: {numerical_grad:.6f}")
    print()

def multivariate_example():
    """Example: f(x,y) = x^2*y + y^3, partial derivatives"""
    print("=== Multivariate Example ===")
    print("f(x,y) = x^2*y + y^3")
    print("∂f/∂x = 2xy, ∂f/∂y = x^2 + 3y^2")
    
    x_val, y_val = 2.0, 1.5
    
    # Automatic differentiation
    x = Variable(x_val)
    y = Variable(y_val)
    z = x*x*y + y*y*y
    z.backward()
    
    # Numerical partial derivatives
    f = lambda vars: vars[0]**2 * vars[1] + vars[1]**3
    numerical_dx = NumericalGradient.partial_gradient(f, [x_val, y_val], 0)
    numerical_dy = NumericalGradient.partial_gradient(f, [x_val, y_val], 1)
    
    # Analytical results
    analytical_dx = 2 * x_val * y_val
    analytical_dy = x_val**2 + 3 * y_val**2
    
    print(f"At x = {x_val}, y = {y_val}:")
    print(f"  ∂f/∂x - Auto: {x.grad:.6f}, Numerical: {numerical_dx:.6f}, Analytical: {analytical_dx:.6f}")
    print(f"  ∂f/∂y - Auto: {y.grad:.6f}, Numerical: {numerical_dy:.6f}, Analytical: {analytical_dy:.6f}")
    print()

def neural_network_example():
    """Simple neural network with one hidden layer"""
    print("=== Neural Network Example ===")
    print("Simple network: input -> hidden(2) -> output(1)")

    x = Variable(0.5)
    
    w1 = Variable(0.3)
    w2 = Variable(-0.1)
    b1 = Variable(0.1)
    b2 = Variable(0.2)
    

    w3 = Variable(0.4)
    w4 = Variable(0.6)
    b3 = Variable(-0.1)
    
    h1 = (x * w1 + b1).tanh()
    h2 = (x * w2 + b2).tanh()
    output = h1 * w3 + h2 * w4 + b3
    
    output.backward()
    
    print(f"Input: {x.data:.3f}")
    print(f"Hidden layer outputs: h1={h1.data:.3f}, h2={h2.data:.3f}")
    print(f"Final output: {output.data:.3f}")
    print("\nGradients:")
    print(f"  ∂L/∂w1 = {w1.grad:.6f}")
    print(f"  ∂L/∂w2 = {w2.grad:.6f}")
    print(f"  ∂L/∂w3 = {w3.grad:.6f}")
    print(f"  ∂L/∂w4 = {w4.grad:.6f}")
    print(f"  ∂L/∂b1 = {b1.grad:.6f}")
    print(f"  ∂L/∂b2 = {b2.grad:.6f}")
    print(f"  ∂L/∂b3 = {b3.grad:.6f}")
    print()

def gradient_descent_example():
    """Optimize a simple function using computed gradients"""
    print("=== Gradient Descent Example ===")
    print("Minimizing f(x) = (x - 2)^2 + 1")
    print("Minimum should be at x = 2")
    
    x_val = 0.0  # Starting point
    learning_rate = 0.1
    history = []
    
    for i in range(20):
        x = Variable(x_val)
        y = (x - 2)**2 + 1  # (x - 2)^2 + 1
        y.backward()
        
        history.append((x_val, y.data))

        x_val = x_val - learning_rate * x.grad
        
        if i % 5 == 0:
            print(f"Step {i:2d}: x = {x_val:.6f}, f(x) = {y.data:.6f}, grad = {x.grad:.6f}")
    
    print(f"Final: x = {x_val:.6f}, close to optimal x = 2.0")
    print()

if __name__ == "__main__":
    # Run all examples
    simple_function_example()
    complex_function_example()
    multivariate_example()
    neural_network_example()
    gradient_descent_example()
    
    print("=== Summary ===")
    print("This implementation demonstrates:")
    print("1. Automatic differentiation using computational graphs")
    print("2. Forward and backward passes")
    print("3. Chain rule application")
    print("4. Comparison with numerical differentiation")
    print("5. Applications to neural networks and optimization")