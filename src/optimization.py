"""Optimization functions for workshop investment problem."""
import numpy as np
from scipy.optimize import minimize


def income1(x):
    """Calculate income for workshop 1.

    Args:
        x: Investment amount

    Returns:
        Income from workshop 1
    """
    return 80 + 0.7 * x**(3/4)


def income2(x):
    """Calculate income for workshop 2.

    Args:
        x: Investment amount

    Returns:
        Income from workshop 2
    """
    return 50 + 1.5 * x**(2/3)


def remainder1(x):
    """Calculate remainder for workshop 1.

    Args:
        x: Investment amount

    Returns:
        Remainder from workshop 1
    """
    return 0.63 * x


def remainder2(x):
    """Calculate remainder for workshop 2.

    Args:
        x: Investment amount

    Returns:
        Remainder from workshop 2
    """
    return 0.79 * x


def f(x):
    """Calculate total revenue for workshop 1.

    Args:
        x: Investment amount

    Returns:
        Total revenue (income + remainder) for workshop 1
    """
    return income1(x) + remainder1(x)


def g(x):
    """Calculate total revenue for workshop 2.

    Args:
        x: Investment amount

    Returns:
        Total revenue (income + remainder) for workshop 2
    """
    return income2(x) + remainder2(x)


def goalFunc(x):
    """Negative goal function for minimization.

    Args:
        x: Array with [investment1, investment2]

    Returns:
        Negative total revenue (for minimization)
    """
    return -(f(x[0]) + g(x[1]))


def optimize_brute_force(total, step_size=0.01):
    """Optimize investments using brute force approach.

    Args:
        total: Total investment amount available
        step_size: Step size for search grid

    Returns:
        Tuple of (optimal_x, optimal_y, maximum_revenue)
    """
    maximum = 0
    optimal_x, optimal_y = 0, 0
    num_samples = int(total / step_size) + 1
    ls = np.linspace(0, total, num_samples)

    for x in ls:
        y = total - x
        revenue = -goalFunc([x, y])
        if revenue > maximum:
            maximum = revenue
            optimal_x = x
            optimal_y = y

    return optimal_x, optimal_y, maximum


def optimize_scipy(total, initial_guess=None):
    """Optimize investments using scipy minimize.

    Args:
        total: Total investment amount available
        initial_guess: Initial guess for optimization (default: [0, total])

    Returns:
        Tuple of (optimal_x, optimal_y, maximum_revenue)
    """
    if initial_guess is None:
        initial_guess = [0, total]

    # Constraints
    constraints = [
        {'type': 'eq', 'fun': lambda x: x[0] + x[1] - total},
        {'type': 'ineq', 'fun': lambda x: x[0]},
        {'type': 'ineq', 'fun': lambda x: x[1]},
    ]

    res = minimize(goalFunc, initial_guess, constraints=constraints)

    return res.x[0], res.x[1], -res.fun


def simulate_quarters(initial_total, num_quarters=4, method='scipy'):
    """Simulate multiple quarters of investment optimization.

    Args:
        initial_total: Initial total investment amount
        num_quarters: Number of quarters to simulate
        method: Optimization method ('scipy' or 'brute_force')

    Returns:
        List of tuples, each containing (quarter, optimal_x, optimal_y, maximum_revenue)
    """
    total = initial_total
    results = []

    for i in range(num_quarters):
        if method == 'scipy':
            optimal_x, optimal_y, maximum = optimize_scipy(total)
        elif method == 'brute_force':
            optimal_x, optimal_y, maximum = optimize_brute_force(total)
        else:
            raise ValueError(f"Unknown method: {method}")

        total = maximum
        results.append((i + 1, optimal_x, optimal_y, maximum))

    return results
