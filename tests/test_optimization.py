"""Tests for optimization module."""
import pytest
import numpy as np
from src.optimization import (
    income1, income2, remainder1, remainder2,
    f, g, goalFunc,
    optimize_brute_force, optimize_scipy, simulate_quarters
)


class TestIncomeFunction1:
    """Test income1 function."""

    def test_zero_investment(self):
        """Test with zero investment."""
        assert income1(0) == 80

    def test_positive_investment(self):
        """Test with positive investment."""
        result = income1(100)
        expected = 80 + 0.7 * 100**(3/4)
        assert abs(result - expected) < 1e-10

    def test_small_investment(self):
        """Test with small investment."""
        result = income1(1)
        expected = 80 + 0.7 * 1**(3/4)
        assert abs(result - expected) < 1e-10

    def test_large_investment(self):
        """Test with large investment."""
        result = income1(1000)
        expected = 80 + 0.7 * 1000**(3/4)
        assert abs(result - expected) < 1e-10

    def test_fractional_investment(self):
        """Test with fractional investment."""
        result = income1(4.92)
        assert result > 80  # Should be greater than base income


class TestIncomeFunction2:
    """Test income2 function."""

    def test_zero_investment(self):
        """Test with zero investment."""
        assert income2(0) == 50

    def test_positive_investment(self):
        """Test with positive investment."""
        result = income2(100)
        expected = 50 + 1.5 * 100**(2/3)
        assert abs(result - expected) < 1e-10

    def test_small_investment(self):
        """Test with small investment."""
        result = income2(1)
        expected = 50 + 1.5 * 1**(2/3)
        assert abs(result - expected) < 1e-10

    def test_large_investment(self):
        """Test with large investment."""
        result = income2(1000)
        expected = 50 + 1.5 * 1000**(2/3)
        assert abs(result - expected) < 1e-10

    def test_fractional_investment(self):
        """Test with fractional investment."""
        result = income2(140.08)
        assert result > 50  # Should be greater than base income


class TestRemainderFunction1:
    """Test remainder1 function."""

    def test_zero_investment(self):
        """Test with zero investment."""
        assert remainder1(0) == 0

    def test_positive_investment(self):
        """Test with positive investment."""
        assert remainder1(100) == 63

    def test_small_investment(self):
        """Test with small investment."""
        assert remainder1(10) == 6.3

    def test_large_investment(self):
        """Test with large investment."""
        assert remainder1(1000) == 630

    def test_coefficient(self):
        """Test that coefficient is exactly 0.63."""
        x = 123.45
        assert remainder1(x) == 0.63 * x


class TestRemainderFunction2:
    """Test remainder2 function."""

    def test_zero_investment(self):
        """Test with zero investment."""
        assert remainder2(0) == 0

    def test_positive_investment(self):
        """Test with positive investment."""
        assert remainder2(100) == 79

    def test_small_investment(self):
        """Test with small investment."""
        assert remainder2(10) == 7.9

    def test_large_investment(self):
        """Test with large investment."""
        assert remainder2(1000) == 790

    def test_coefficient(self):
        """Test that coefficient is exactly 0.79."""
        x = 123.45
        assert remainder2(x) == 0.79 * x


class TestTotalRevenueF:
    """Test f function (total revenue for workshop 1)."""

    def test_zero_investment(self):
        """Test with zero investment."""
        assert f(0) == 80

    def test_positive_investment(self):
        """Test with positive investment."""
        x = 100
        expected = income1(x) + remainder1(x)
        assert f(x) == expected

    def test_composition(self):
        """Test that f is composition of income1 and remainder1."""
        for x in [0, 10, 50, 100, 500]:
            assert f(x) == income1(x) + remainder1(x)


class TestTotalRevenueG:
    """Test g function (total revenue for workshop 2)."""

    def test_zero_investment(self):
        """Test with zero investment."""
        assert g(0) == 50

    def test_positive_investment(self):
        """Test with positive investment."""
        x = 100
        expected = income2(x) + remainder2(x)
        assert g(x) == expected

    def test_composition(self):
        """Test that g is composition of income2 and remainder2."""
        for x in [0, 10, 50, 100, 500]:
            assert g(x) == income2(x) + remainder2(x)


class TestGoalFunction:
    """Test goalFunc."""

    def test_zero_investment(self):
        """Test with zero investment."""
        result = goalFunc([0, 0])
        expected = -(f(0) + g(0))
        assert result == expected

    def test_positive_investment(self):
        """Test with positive investment."""
        result = goalFunc([100, 50])
        expected = -(f(100) + g(50))
        assert abs(result - expected) < 1e-10

    def test_is_negative(self):
        """Test that result is negative (for minimization)."""
        result = goalFunc([100, 100])
        assert result < 0

    def test_different_allocations(self):
        """Test with different allocations."""
        result1 = goalFunc([50, 50])
        result2 = goalFunc([75, 25])
        result3 = goalFunc([25, 75])
        # All should be negative
        assert result1 < 0
        assert result2 < 0
        assert result3 < 0

    def test_single_investment(self):
        """Test with all investment in one workshop."""
        result1 = goalFunc([100, 0])
        result2 = goalFunc([0, 100])
        assert result1 < 0
        assert result2 < 0


class TestOptimizeBruteForce:
    """Test optimize_brute_force function."""

    def test_small_investment(self):
        """Test with small investment."""
        optimal_x, optimal_y, maximum = optimize_brute_force(10, step_size=0.1)
        assert optimal_x >= 0
        assert optimal_y >= 0
        assert abs(optimal_x + optimal_y - 10) < 0.2  # Within step tolerance
        assert maximum > 0

    def test_medium_investment(self):
        """Test with medium investment."""
        optimal_x, optimal_y, maximum = optimize_brute_force(145, step_size=0.1)
        assert optimal_x >= 0
        assert optimal_y >= 0
        assert abs(optimal_x + optimal_y - 145) < 0.2  # Within step tolerance
        assert maximum > 0

    def test_zero_investment(self):
        """Test with zero investment."""
        optimal_x, optimal_y, maximum = optimize_brute_force(0, step_size=0.01)
        assert optimal_x == 0
        assert optimal_y == 0
        assert maximum == 130  # income1(0) + income2(0)

    def test_return_types(self):
        """Test return types."""
        optimal_x, optimal_y, maximum = optimize_brute_force(100)
        assert isinstance(optimal_x, (int, float, np.number))
        assert isinstance(optimal_y, (int, float, np.number))
        assert isinstance(maximum, (int, float, np.number))

    def test_different_step_sizes(self):
        """Test with different step sizes."""
        result1 = optimize_brute_force(100, step_size=1.0)
        result2 = optimize_brute_force(100, step_size=0.1)
        # Smaller step size should give similar or better result
        assert result2[2] >= result1[2] - 1  # Allow small tolerance

    def test_large_investment(self):
        """Test with large investment."""
        optimal_x, optimal_y, maximum = optimize_brute_force(1000, step_size=1.0)
        assert optimal_x >= 0
        assert optimal_y >= 0
        assert maximum > 0


class TestOptimizeScipy:
    """Test optimize_scipy function."""

    def test_small_investment(self):
        """Test with small investment."""
        optimal_x, optimal_y, maximum = optimize_scipy(10)
        assert optimal_x >= 0
        assert optimal_y >= 0
        assert abs(optimal_x + optimal_y - 10) < 1e-6
        assert maximum > 0

    def test_medium_investment(self):
        """Test with medium investment - matches notebook result."""
        optimal_x, optimal_y, maximum = optimize_scipy(145)
        assert optimal_x >= 0
        assert optimal_y >= 0
        assert abs(optimal_x + optimal_y - 145) < 1e-6
        # Should be close to notebook result: 286.533...
        assert abs(maximum - 286.533) < 1

    def test_very_small_investment(self):
        """Test with very small investment."""
        optimal_x, optimal_y, maximum = optimize_scipy(0.1)
        assert optimal_x >= 0
        assert optimal_y >= 0
        assert abs(optimal_x + optimal_y - 0.1) < 1e-6
        # Should be close to base income (130) plus small amount
        assert maximum > 130

    def test_custom_initial_guess(self):
        """Test with custom initial guess."""
        optimal_x, optimal_y, maximum = optimize_scipy(100, initial_guess=[50, 50])
        assert optimal_x >= 0
        assert optimal_y >= 0
        assert abs(optimal_x + optimal_y - 100) < 1e-6

    def test_return_types(self):
        """Test return types."""
        optimal_x, optimal_y, maximum = optimize_scipy(100)
        assert isinstance(optimal_x, (int, float, np.number))
        assert isinstance(optimal_y, (int, float, np.number))
        assert isinstance(maximum, (int, float, np.number))

    def test_large_investment(self):
        """Test with large investment."""
        optimal_x, optimal_y, maximum = optimize_scipy(1000)
        assert optimal_x >= 0
        assert optimal_y >= 0
        assert abs(optimal_x + optimal_y - 1000) < 1e-6
        assert maximum > 0

    def test_fractional_investment(self):
        """Test with fractional investment."""
        optimal_x, optimal_y, maximum = optimize_scipy(286.533)
        assert optimal_x >= 0
        assert optimal_y >= 0
        assert abs(optimal_x + optimal_y - 286.533) < 1e-6


class TestSimulateQuarters:
    """Test simulate_quarters function."""

    def test_scipy_method(self):
        """Test with scipy method."""
        results = simulate_quarters(145, num_quarters=4, method='scipy')
        assert len(results) == 4
        # Check first quarter matches notebook
        quarter1 = results[0]
        assert quarter1[0] == 1
        assert quarter1[1] >= 0  # optimal_x
        assert quarter1[2] >= 0  # optimal_y
        assert abs(quarter1[3] - 286.533) < 1  # maximum

    def test_brute_force_method(self):
        """Test with brute force method."""
        results = simulate_quarters(145, num_quarters=4, method='brute_force')
        assert len(results) == 4
        # Check structure
        for i, result in enumerate(results):
            assert result[0] == i + 1  # Quarter number
            assert result[1] >= 0  # optimal_x
            assert result[2] >= 0  # optimal_y
            assert result[3] > 0  # maximum

    def test_single_quarter(self):
        """Test with single quarter."""
        results = simulate_quarters(100, num_quarters=1, method='scipy')
        assert len(results) == 1
        assert results[0][0] == 1

    def test_invalid_method(self):
        """Test with invalid method."""
        with pytest.raises(ValueError, match="Unknown method"):
            simulate_quarters(100, method='invalid_method')

    def test_zero_quarters(self):
        """Test with zero quarters."""
        results = simulate_quarters(100, num_quarters=0)
        assert len(results) == 0

    def test_growing_total(self):
        """Test that total grows each quarter."""
        results = simulate_quarters(145, num_quarters=4, method='scipy')
        for i in range(len(results) - 1):
            # Each quarter's maximum should be greater than previous total
            assert results[i + 1][3] > results[i][3]

    def test_two_quarters(self):
        """Test with two quarters."""
        results = simulate_quarters(145, num_quarters=2, method='scipy')
        assert len(results) == 2
        # Second quarter should have higher revenue
        assert results[1][3] > results[0][3]

    def test_scipy_vs_brute_force_similarity(self):
        """Test that both methods give similar results."""
        scipy_results = simulate_quarters(100, num_quarters=2, method='scipy')
        brute_results = simulate_quarters(100, num_quarters=2, method='brute_force')
        # Results should be similar (within 5%)
        for i in range(2):
            assert abs(scipy_results[i][3] - brute_results[i][3]) / scipy_results[i][3] < 0.05

    def test_large_initial_investment(self):
        """Test with large initial investment."""
        results = simulate_quarters(1000, num_quarters=2, method='scipy')
        assert len(results) == 2
        assert all(r[3] > 0 for r in results)

    def test_small_initial_investment(self):
        """Test with small initial investment."""
        results = simulate_quarters(10, num_quarters=2, method='scipy')
        assert len(results) == 2
        assert all(r[3] > 0 for r in results)
