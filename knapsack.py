'''def knapSack(W, wt, val, n):
 
    # Base Case
    if n == 0 or W == 0:
        return 0
 
    # If weight of the nth item is
    # more than Knapsack of capacity W,
    # then this item cannot be included
    # in the optimal solution
    if (wt[n-1] > W):
        return knapSack(W, wt, val, n-1)
 
    # return the maximum of two cases:
    # (1) nth item included
    # (2) not included
    else:
        return max(val[n-1] + knapSack(W-wt[n-1], wt, val, n-1), knapSack(W, wt, val, n-1))


if __name__ == '__main__':
    # problem = {'val': [60, 100, 120, 50], 'wt': [10, 20, 30, 5], 'W': 50}
    problem = {
        'val': [
            360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147, 78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28, 87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276, 312
        ],
        'wt': [
            7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0, 42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71, 3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13
        ],
        'W': 850
    }
    print(knapSack(problem['W'], problem['wt'], problem['val'], len(problem['val'])))'''



from ortools.algorithms import pywrapknapsack_solver


def main():
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    '''values = [
        360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
        78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
        87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
        312
    ]
    weights = [[
        7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
        42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
        3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13
    ]]
    capacities = [850]'''

    values = [
        3, 5, 1, 7, 10, 8, 10, 6, 0, 2, 0, 5, 7, 1, 4, 4, 3, 7, 7, 3, 10, 3, 7, 6, 3, 10, 9, 9, 2, 7, 1, 10, 2, 2, 0, 1, 5, 0, 10, 4, 10, 8, 10, 4, 5, 8, 1, 8, 6, 7, 2, 3, 10, 7, 8, 1, 6, 8, 0, 8,
        2, 0, 9, 4, 4, 5, 1, 1, 7, 10, 1, 1, 8, 1, 9, 7, 8, 3, 2, 8, 10, 5, 1, 0, 4, 5, 9, 10, 2, 2, 4, 1, 1, 10, 8, 6, 10, 0, 6, 4
    ]
    weights = [[
        5, 0, 5, 1, 10, 8, 5, 5, 3, 7, 1, 0, 7, 5, 0, 9, 7, 4, 10, 0, 5, 8, 3, 9, 9, 1, 3, 4, 6, 2, 8, 5, 6, 0, 8, 4, 9, 6, 6, 10, 8, 9, 10, 8, 7, 2, 7, 1, 0, 6, 10, 9, 1, 6, 2, 6, 10, 9, 1, 8, 3,
        7, 7, 9, 2, 7, 0, 1, 10, 9, 6, 2,9, 9, 8, 3, 3, 10, 2, 10, 5, 8, 6, 1, 3, 10, 6, 0, 8, 4, 10, 9, 8, 7, 4, 5, 2, 0, 10, 6
    ]]
    capacities = [450]

    solver.Init(values, weights, capacities)
    computed_value = solver.Solve()

    packed_items = []
    packed_weights = []
    total_weight = 0
    print('Total value =', computed_value)
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    print('Total weight:', total_weight)
    print('Packed items:', packed_items)
    print('Packed_weights:', packed_weights)


if __name__ == '__main__':
    main()
    
    '''import pandas as pd

    res = []
    freqs = [0.25, 0.5, 0.75]
    replace_n = [0.1, 0.25, 0.5]
    method = [1, 2, 3]

    res.append(["config_0", 0, 0, 0])
    count = 1
    for i in freqs:
        for j in replace_n:
            for k in method:
                res.append([f"config_{count}", i, j, k])
                count += 1

    df = pd.DataFrame(res, columns=["Name", "Frequency", "% of replacement", "Method"])
    df.set_index("Name")
    df.to_csv("configs.csv", index=False)

    print(df)
'''