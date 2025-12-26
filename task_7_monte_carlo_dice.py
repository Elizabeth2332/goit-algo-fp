import random
from collections import Counter

import matplotlib.pyplot as plt


def analytical_probabilities():
    """
    Аналітичні ймовірності для суми двох чесних кубиків.
    Кількість комбінацій = 36.
    """
    counts = {
        2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6,
        8: 5, 9: 4, 10: 3, 11: 2, 12: 1
    }
    probs = {s: c / 36 for s, c in counts.items()}
    return counts, probs


def monte_carlo_simulation(n_rolls: int, seed: int = 42):
    random.seed(seed)
    sums = []
    for _ in range(n_rolls):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        sums.append(d1 + d2)

    counts = Counter(sums)
    probs = {s: counts.get(s, 0) / n_rolls for s in range(2, 13)}
    return counts, probs


def print_table(n_rolls, mc_counts, mc_probs, an_counts, an_probs):
    print("=" * 80)
    print(f"Monte Carlo simulation for two dice (rolls = {n_rolls})")
    print("=" * 80)
    header = f"{'Sum':>3} | {'MC count':>8} | {'MC prob':>8} | {'Analytic':>8} | {'Abs diff':>8}"
    print(header)
    print("-" * len(header))

    for s in range(2, 13):
        mc_p = mc_probs[s]
        an_p = an_probs[s]
        diff = abs(mc_p - an_p)
        print(f"{s:>3} | {mc_counts.get(s, 0):>8} | {mc_p:>8.4f} | {an_p:>8.4f} | {diff:>8.4f}")


def plot_probs(mc_probs, an_probs, n_rolls):
    sums = list(range(2, 13))
    mc_vals = [mc_probs[s] for s in sums]
    an_vals = [an_probs[s] for s in sums]

    plt.figure(figsize=(10, 5))
    plt.plot(sums, mc_vals, marker="o", linestyle="-", label=f"Monte Carlo (N={n_rolls})")
    plt.plot(sums, an_vals, marker="s", linestyle="--", label="Analytical")
    plt.xticks(sums)
    plt.xlabel("Sum (two dice)")
    plt.ylabel("Probability")
    plt.title("Two Dice Sum Probabilities: Monte Carlo vs Analytical")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    # можеш збільшити N для кращої точності
    n_rolls = 200_000

    an_counts, an_probs = analytical_probabilities()
    mc_counts, mc_probs = monte_carlo_simulation(n_rolls, seed=42)

    print_table(n_rolls, mc_counts, mc_probs, an_counts, an_probs)
    plot_probs(mc_probs, an_probs, n_rolls)

    # Короткий висновок
    max_abs_diff = max(abs(mc_probs[s] - an_probs[s]) for s in range(2, 13))
    print("\nConclusion:")
    print(f"Max absolute difference between Monte Carlo and analytical probabilities: {max_abs_diff:.5f}")
    print("With larger N, Monte Carlo probabilities converge to analytical values.")


if __name__ == "__main__":
    main()
