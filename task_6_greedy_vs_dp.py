from typing import Dict, List, Tuple

items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}


def greedy_algorithm(items: Dict[str, Dict[str, int]], budget: int) -> Tuple[List[str], int, int]:
    """
    Greedy: choose by maximum calories/cost ratio, without exceeding budget.
    0/1 choice (each item at most once).
    Returns: (chosen_items, total_cost, total_calories)
    """
    ranked = sorted(
        items.items(),
        key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
        reverse=True,
    )

    chosen = []
    total_cost = 0
    total_cal = 0

    for name, info in ranked:
        if total_cost + info["cost"] <= budget:
            chosen.append(name)
            total_cost += info["cost"]
            total_cal += info["calories"]

    return chosen, total_cost, total_cal


def dynamic_programming(items: Dict[str, Dict[str, int]], budget: int) -> Tuple[List[str], int, int]:
    """
    DP (0/1 knapsack): maximize calories under cost<=budget.
    Returns: (chosen_items, total_cost, total_calories)
    """
    names = list(items.keys())
    n = len(names)

    # dp[i][b] = max calories using first i items within budget b
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name = names[i - 1]
        cost = items[name]["cost"]
        cal = items[name]["calories"]

        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]  # skip
            if cost <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + cal)

    # reconstruct chosen items
    chosen = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            name = names[i - 1]
            chosen.append(name)
            b -= items[name]["cost"]

    chosen.reverse()

    total_cost = sum(items[name]["cost"] for name in chosen)
    total_cal = sum(items[name]["calories"] for name in chosen)

    return chosen, total_cost, total_cal


def print_result(title: str, chosen: List[str], total_cost: int, total_cal: int, budget: int):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    print(f"Budget: {budget}")
    print(f"Chosen items: {chosen}")
    print(f"Total cost: {total_cost}")
    print(f"Total calories: {total_cal}")


if __name__ == "__main__":
    budget = 100  

    g_items, g_cost, g_cal = greedy_algorithm(items, budget)
    dp_items, dp_cost, dp_cal = dynamic_programming(items, budget)

    print_result("Greedy algorithm (calories/cost)", g_items, g_cost, g_cal, budget)
    print_result("Dynamic programming (optimal)", dp_items, dp_cost, dp_cal, budget)

    print("\nComparison:")
    if dp_cal > g_cal:
        print(f"DP is better by {dp_cal - g_cal} calories.")
    elif dp_cal < g_cal:
        print(f"Greedy is better by {g_cal - dp_cal} calories (rare, depends on data).")
    else:
        print("Greedy equals DP for this budget.")
