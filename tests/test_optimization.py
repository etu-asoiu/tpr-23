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


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_income1_very_large_value(self):
        """Test income1 with very large investment."""
        result = income1(1_000_000)
        assert result > 80
        assert np.isfinite(result)

    def test_income2_very_large_value(self):
        """Test income2 with very large investment."""
        result = income2(1_000_000)
        assert result > 50
        assert np.isfinite(result)

    def test_remainder_negative_input(self):
        """Test remainder functions handle negative inputs."""
        # Mathematically, these functions work with negative inputs
        assert remainder1(-100) == -63
        assert remainder2(-100) == -79

    def test_fractional_powers_with_decimals(self):
        """Test fractional power calculations with various decimals."""
        test_values = [0.5, 1.5, 2.7, 10.3, 99.9]
        for val in test_values:
            assert np.isfinite(income1(val))
            assert np.isfinite(income2(val))
            assert income1(val) > 80
            assert income2(val) > 50

    def test_goalFunc_symmetry(self):
        """Test goal function with symmetrical inputs."""
        result1 = goalFunc([100, 200])
        result2 = goalFunc([200, 100])
        # Results should be different due to different workshop functions
        assert result1 != result2

    def test_optimize_with_equal_split(self):
        """Test optimization starting with equal split."""
        total = 200
        optimal_x, optimal_y, maximum = optimize_scipy(total, initial_guess=[100, 100])
        assert abs(optimal_x + optimal_y - total) < 1e-6
        assert maximum > 0


class TestPropertyBasedTests:
    """Property-based tests for mathematical properties."""

    def test_income1_monotonicity(self):
        """Test that income1 is monotonically increasing."""
        values = [0, 10, 50, 100, 200, 500]
        results = [income1(v) for v in values]
        for i in range(len(results) - 1):
            assert results[i] < results[i + 1], f"income1 not monotonic at {values[i]}"

    def test_income2_monotonicity(self):
        """Test that income2 is monotonically increasing."""
        values = [0, 10, 50, 100, 200, 500]
        results = [income2(v) for v in values]
        for i in range(len(results) - 1):
            assert results[i] < results[i + 1], f"income2 not monotonic at {values[i]}"

    def test_remainder_linearity(self):
        """Test that remainder functions are linear."""
        x = 100
        # Test scaling property
        assert remainder1(2 * x) == 2 * remainder1(x)
        assert remainder2(2 * x) == 2 * remainder2(x)
        # Test additive property
        y = 50
        assert abs(remainder1(x + y) - (remainder1(x) + remainder1(y))) < 1e-10
        assert abs(remainder2(x + y) - (remainder2(x) + remainder2(y))) < 1e-10

    def test_total_revenue_monotonicity(self):
        """Test that total revenue functions are monotonically increasing."""
        values = [0, 10, 50, 100, 200, 500]
        f_results = [f(v) for v in values]
        g_results = [g(v) for v in values]
        for i in range(len(values) - 1):
            assert f_results[i] < f_results[i + 1]
            assert g_results[i] < g_results[i + 1]

    def test_optimization_constraint_satisfaction(self):
        """Test that optimization satisfies budget constraint."""
        totals = [10, 50, 100, 200, 500]
        for total in totals:
            optimal_x, optimal_y, maximum = optimize_scipy(total)
            # Budget constraint: x + y = total
            assert abs(optimal_x + optimal_y - total) < 1e-6
            # Non-negativity constraints
            assert optimal_x >= -1e-6
            assert optimal_y >= -1e-6

    def test_revenue_sum_property(self):
        """Test that total revenue is sum of workshop revenues."""
        test_allocations = [[50, 50], [25, 75], [75, 25], [10, 90]]
        for x, y in test_allocations:
            total_revenue = f(x) + g(y)
            assert abs(-goalFunc([x, y]) - total_revenue) < 1e-10


class TestIntegrationTests:
    """Integration tests matching notebook results."""

    def test_first_quarter_optimization(self):
        """Test first quarter optimization matches notebook."""
        initial_total = 145
        optimal_x, optimal_y, maximum = optimize_scipy(initial_total)

        # From notebook: optimal_x ≈ 4.917, optimal_y ≈ 140.082, maximum ≈ 286.533
        assert abs(optimal_x - 4.917) < 0.01
        assert abs(optimal_y - 140.082) < 0.01
        assert abs(maximum - 286.533) < 0.01

    def test_four_quarters_simulation(self):
        """Test four quarters simulation matches notebook pattern."""
        results = simulate_quarters(145, num_quarters=4, method='scipy')

        # From notebook results
        expected_revenues = [286.533, 422.386, 549.126, 665.519]

        for i, (quarter, _, _, revenue) in enumerate(results):
            assert quarter == i + 1
            # Allow 1% tolerance
            assert abs(revenue - expected_revenues[i]) < expected_revenues[i] * 0.01

    def test_quarter_growth_rate(self):
        """Test that revenue grows at decreasing rate each quarter."""
        results = simulate_quarters(145, num_quarters=4, method='scipy')
        revenues = [r[3] for r in results]

        # Calculate growth rates
        growth_rates = []
        for i in range(len(revenues) - 1):
            growth_rate = (revenues[i + 1] - revenues[i]) / revenues[i]
            growth_rates.append(growth_rate)

        # Growth rates should be positive but decreasing
        for i in range(len(growth_rates) - 1):
            assert growth_rates[i] > 0
            assert growth_rates[i] > growth_rates[i + 1]

    def test_optimal_allocation_pattern(self):
        """Test that workshop 2 gets more investment (as per notebook)."""
        results = simulate_quarters(145, num_quarters=4, method='scipy')

        for quarter, optimal_x, optimal_y, _ in results:
            # Workshop 2 should get more investment
            assert optimal_y > optimal_x


class TestValidationTests:
    """Validation tests for correctness and consistency."""

    def test_optimization_improves_naive_split(self):
        """Test that optimization beats naive 50-50 split."""
        total = 200

        # Naive split
        naive_revenue = -goalFunc([total/2, total/2])

        # Optimized split
        optimal_x, optimal_y, optimal_revenue = optimize_scipy(total)

        assert optimal_revenue >= naive_revenue

    def test_brute_force_finds_near_optimal(self):
        """Test that brute force finds solution close to scipy."""
        total = 100

        scipy_x, scipy_y, scipy_max = optimize_scipy(total)
        brute_x, brute_y, brute_max = optimize_brute_force(total, step_size=0.1)

        # Should be within 1% of each other
        assert abs(brute_max - scipy_max) < scipy_max * 0.01

    def test_consistency_across_runs(self):
        """Test that optimization gives consistent results."""
        total = 150

        results = []
        for _ in range(3):
            optimal_x, optimal_y, maximum = optimize_scipy(total)
            results.append((optimal_x, optimal_y, maximum))

        # All runs should give same result
        for i in range(1, len(results)):
            assert abs(results[i][0] - results[0][0]) < 1e-6
            assert abs(results[i][1] - results[0][1]) < 1e-6
            assert abs(results[i][2] - results[0][2]) < 1e-6

    def test_simulation_quarter_sequence(self):
        """Test that quarter numbers are correctly sequenced."""
        results = simulate_quarters(100, num_quarters=5, method='scipy')

        quarters = [r[0] for r in results]
        assert quarters == [1, 2, 3, 4, 5]

    def test_revenue_components_positive(self):
        """Test that income and remainder components are positive for positive investment."""
        x = 100
        assert income1(x) > 0
        assert income2(x) > 0
        assert remainder1(x) > 0
        assert remainder2(x) > 0
        assert f(x) > 0
        assert g(x) > 0


class TestNumericalStability:
    """Test numerical stability and precision."""

    def test_small_differences_detection(self):
        """Test that small differences in input produce different outputs."""
        x1 = 100.0
        x2 = 100.1

        assert income1(x1) != income1(x2)
        assert income2(x1) != income2(x2)

    def test_optimization_precision(self):
        """Test optimization achieves high precision."""
        total = 145
        optimal_x, optimal_y, maximum = optimize_scipy(total)

        # Verify constraint is satisfied to high precision
        assert abs(optimal_x + optimal_y - total) < 1e-10

    def test_large_number_handling(self):
        """Test handling of large investment amounts."""
        large_total = 10_000
        optimal_x, optimal_y, maximum = optimize_scipy(large_total)

        assert np.isfinite(optimal_x)
        assert np.isfinite(optimal_y)
        assert np.isfinite(maximum)
        assert maximum > 0

    def test_very_small_number_handling(self):
        """Test handling of very small investment amounts."""
        small_total = 0.01
        optimal_x, optimal_y, maximum = optimize_scipy(small_total)

        assert np.isfinite(optimal_x)
        assert np.isfinite(optimal_y)
        assert np.isfinite(maximum)
        assert abs(optimal_x + optimal_y - small_total) < 1e-10


class TestPerformanceComparisons:
    """Test performance characteristics of different methods."""

    def test_scipy_efficiency(self):
        """Test that scipy method completes in reasonable time."""
        import time

        total = 1000
        start_time = time.time()
        optimize_scipy(total)
        elapsed_time = time.time() - start_time

        # Should complete in less than 1 second
        assert elapsed_time < 1.0

    def test_brute_force_step_size_impact(self):
        """Test that smaller step size improves brute force accuracy."""
        total = 100

        _, _, max1 = optimize_brute_force(total, step_size=1.0)
        _, _, max2 = optimize_brute_force(total, step_size=0.1)
        _, _, max3 = optimize_brute_force(total, step_size=0.01)

        # Smaller step size should give better or equal result
        assert max2 >= max1 - 0.1
        assert max3 >= max2 - 0.1

    def test_method_comparison_on_multiple_totals(self):
        """Compare scipy and brute force on multiple investment amounts."""
        totals = [50, 100, 200, 500]

        for total in totals:
            scipy_result = optimize_scipy(total)
            brute_result = optimize_brute_force(total, step_size=0.5)

            # Both should find positive maximum
            assert scipy_result[2] > 0
            assert brute_result[2] > 0
            # Scipy should be at least as good
            assert scipy_result[2] >= brute_result[2] - 1


class TestBoundaryConditions:
    """Test specific boundary conditions."""

    def test_income_at_unity(self):
        """Test income functions at x=1."""
        assert abs(income1(1) - (80 + 0.7)) < 1e-10
        assert abs(income2(1) - (50 + 1.5)) < 1e-10

    def test_remainder_at_unity(self):
        """Test remainder functions at x=1."""
        assert remainder1(1) == 0.63
        assert remainder2(1) == 0.79

    def test_total_revenue_at_unity(self):
        """Test total revenue at x=1."""
        assert abs(f(1) - (80.7 + 0.63)) < 1e-10
        assert abs(g(1) - (51.5 + 0.79)) < 1e-10

    def test_optimization_with_minimum_total(self):
        """Test optimization with very small but positive total."""
        total = 1e-6
        optimal_x, optimal_y, maximum = optimize_scipy(total)

        assert abs(optimal_x + optimal_y - total) < 1e-12
        # Should be close to base income
        assert abs(maximum - 130) < 1

    def test_quarter_simulation_boundary(self):
        """Test simulation with edge case number of quarters."""
        # Single quarter
        results1 = simulate_quarters(100, num_quarters=1)
        assert len(results1) == 1

        # Many quarters
        results10 = simulate_quarters(100, num_quarters=10)
        assert len(results10) == 10

        # Verify monotonic growth
        revenues = [r[3] for r in results10]
        for i in range(len(revenues) - 1):
            assert revenues[i + 1] > revenues[i]


class TestDataTypes:
    """Test with different data types and formats."""

    def test_integer_inputs(self):
        """Test functions with integer inputs."""
        assert isinstance(income1(100), (int, float, np.number))
        assert isinstance(income2(100), (int, float, np.number))
        assert isinstance(f(100), (int, float, np.number))
        assert isinstance(g(100), (int, float, np.number))

    def test_float_inputs(self):
        """Test functions with float inputs."""
        assert isinstance(income1(100.5), (int, float, np.number))
        assert isinstance(income2(100.5), (int, float, np.number))

    def test_numpy_scalar_inputs(self):
        """Test functions with numpy scalar inputs."""
        x = np.float64(100)
        assert np.isfinite(income1(x))
        assert np.isfinite(income2(x))
        assert np.isfinite(f(x))
        assert np.isfinite(g(x))

    def test_optimization_returns_correct_types(self):
        """Test that optimization functions return correct types."""
        result = optimize_scipy(100)
        assert len(result) == 3
        assert all(isinstance(r, (int, float, np.number)) for r in result)

    def test_simulation_returns_list_of_tuples(self):
        """Test that simulation returns correctly formatted results."""
        results = simulate_quarters(100, num_quarters=3)

        assert isinstance(results, list)
        assert len(results) == 3
        for result in results:
            assert isinstance(result, tuple)
            assert len(result) == 4
