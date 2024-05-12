# def max_path(matrix):
#     rows = len(matrix)
#     cols = len(matrix[0])

#     # Create a memoization table to store maximum path sums
#     memo = [[0] * cols for _ in range(rows)]

#     # Initialize the first row and first column
#     memo[0][0] = matrix[0][0]
#     for i in range(1, rows):
#         memo[i][0] = memo[i-1][0] + matrix[i][0]
#     for j in range(1, cols):
#         memo[0][j] = memo[0][j-1] + matrix[0][j]

#     # Fill memoization table
#     for i in range(1, rows):
#         for j in range(1, cols):
#             memo[i][j] = max(memo[i-1][j], memo[i][j-1]) + matrix[i][j]

#     for row in memo:
#         print(row)

#     # Return the maximum path sum
#     return memo[rows-1][cols-1]

# # Example matrix
# matrix = [
#     [12, 10, 3, 4, 7],
#     [8, 2, 15, 10, 8],
#     [7, 6, 4, 3, 12],
#     [3, 20, 8, 9, 10],
#     [14, 16, 12, 11, 7]
# ]

# # Finding the maximum path
# max_path_sum = max_path(matrix)
# print("Maximum path sum:", max_path_sum)
dp = []

def MaximumPathUtil(i, j, grid):
 
    global dp 
     
    # Base condition
    if (i == 0 or j == 0):
        return 0
 
    # If current subproblem is already computed,
    # we simply return its result from the dp table
    if (dp[i][j] != -1):
        return dp[i][j]
 
    # Computing the current subproblem and
    # store the result in the dp table for future use
    dp[i][j] = max(MaximumPathUtil(i, j-1, grid), MaximumPathUtil(i - 1, j, grid)) + grid[i-1][j-1]
    
    return dp[i][j]
 
def MaximumPath(grid):
 
    global dp
  
    # Dimensions of grid[][]
    n = len(grid)
    m = len(grid[0])
 
    # dp table to memoize the subproblem results
    dp = [[-1 for i in range(m + 1)] for j in range(n + 1)]
 
    # dp[n][m] gives the max. path sum
    # from grid[0][0] to grid[n-1][m-1]
    return MaximumPathUtil(n, m, grid)
 
# Driver Code
 
grid = [[12, 10, 3, 4, 7],
    [8, 2, 15, 10, 8],
    [7, 6, 4, 3, 12],
    [3, 20, 8, 9, 10],
    [14, 16, 12, 11, 7]]

print(MaximumPath(grid))
for row in dp:
        print(row)
