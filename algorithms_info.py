algorithms_info = {
    "A*": {
        "title": "A* (A Star)",
        "short_description": "A* finds the shortest path using both path cost and heuristic.",
        "long_description": [
            "A* is widely used in pathfinding and graph traversal. It combines Dijkstra's algorithm with a heuristic to guide the search, efficiently finding the shortest path.",
            "It maintains a tree of paths from the start node, extending the path that minimizes the total cost, which includes the known path length and an estimate of the distance to the goal."
        ],
        "type": "Pathfinding Algorithm",
        "time_complexity": "O(n log n), where n is the number of nodes explored",
        "space_complexity": "O(n), where n is the number of nodes in the grid",
        "common_applications": ["Navigation systems", "Robotics", "Video games"]
    },
    "Bi-A*": {
        "title": "Bidirectional A* (A Star)",
        "short_description": "Bi-A* runs two simultaneous A* searches to reduce search space.",
        "long_description": [
            "Bidirectional A* optimizes pathfinding by running two A* searches: one from the start and another from the goal, meeting in the middle. This reduces the number of nodes explored, making it faster on large grids.",
            "It is especially useful in large search spaces, maintaining the benefits of A* while improving efficiency."
        ],
        "type": "Pathfinding Algorithm",
        "time_complexity": "O(n log n), where n is the number of nodes explored",
        "space_complexity": "O(n), where n is the number of nodes in the grid",
        "common_applications": ["Large-scale graph searches", "Navigation systems", "Artificial intelligence in games"]
    },
    "BFS": {
        "title": "Breadth-First Search (BFS)",
        "short_description": "BFS explores all nodes layer by layer from the start.",
        "long_description": [
            "Breadth-First Search (BFS) is a simple algorithm that explores all nodes at the current depth before moving to the next depth level. It is commonly used in unweighted grids to find the shortest path.",
            "BFS explores neighbors evenly, making it ideal for scenarios where each move has the same cost."
        ],
        "type": "Pathfinding Algorithm",
        "time_complexity": "O(n), where n is the number of nodes in the grid",
        "space_complexity": "O(n)",
        "common_applications": ["Unweighted grids", "Social networks", "Simple pathfinding tasks"]
    },
    "DFS": {
        "title": "Depth-First Search (DFS)",
        "short_description": "DFS explores paths deeply before backtracking.",
        "long_description": [
            "Depth-First Search (DFS) explores as far down a path as possible before backtracking. It is used when every possible path needs to be explored.",
            "Although it doesn't guarantee the shortest path, DFS can be useful in tree traversal and some puzzle-solving contexts."
        ],
        "type": "Pathfinding Algorithm",
        "time_complexity": "O(n), where n is the number of nodes in the grid",
        "space_complexity": "O(n)",
        "common_applications": ["Tree traversal", "Maze generation", "Puzzle solving"]
    },
    "GBFS": {
        "title": "Greedy Best-First Search (GBFS)",
        "short_description": "GBFS selects nodes based on proximity to the goal.",
        "long_description": [
            "Greedy Best-First Search (GBFS) selects the node that seems closest to the goal using a heuristic function. Although it can be faster, it does not guarantee the shortest path and can get stuck in local minima.",
            "GBFS is often used in scenarios where speed is prioritized over path optimality."
        ],
        "type": "Pathfinding Algorithm",
        "time_complexity": "O(n log n), where n is the number of nodes explored",
        "space_complexity": "O(n)",
        "common_applications": ["Heuristic search", "Navigation systems", "Artificial intelligence in games"]
    },
    "JPS": {
        "title": "Jump Point Search (JPS)",
        "short_description": "JPS optimizes A* by skipping unnecessary nodes.",
        "long_description": [
            "Jump Point Search (JPS) is an optimization for grid-based maps, reducing the number of nodes A* needs to explore. It 'jumps' over large sections of the grid to find nodes that are critical for the optimal path.",
            "JPS maintains the optimality of A* while improving efficiency, particularly in large grids."
        ],
        "type": "Pathfinding Algorithm",
        "time_complexity": "O(n log n), where n is the number of nodes explored",
        "space_complexity": "O(n)",
        "common_applications": ["Grid-based pathfinding", "Robotics", "Video games"]
    },
    "Manhattan": {
        "title": "Manhattan Heuristic",
        "short_description": "Calculates distance by summing horizontal and vertical moves.",
        "long_description": [
            "The Manhattan heuristic is used to calculate the shortest path between two points on a grid where movement is restricted to horizontal and vertical directions. The distance is the sum of the absolute differences in x and y coordinates."
        ],
        "type": "Heuristic Function",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
        "common_applications": ["Grid-based pathfinding", "2D maps", "Games"]
    },
    "Euclidean": {
        "title": "Euclidean Heuristic",
        "short_description": "Calculates the straight-line distance between two points.",
        "long_description": [
            "The Euclidean heuristic calculates the straight-line distance between two points on a grid. This is useful in situations where diagonal movement is allowed and considered more accurate than Manhattan when diagonal movement is possible."
        ],
        "type": "Heuristic Function",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
        "common_applications": ["Pathfinding with diagonal movement", "3D games", "Robotics"]
    },
    "Diagonal": {
        "title": "Diagonal Heuristic",
        "short_description": "Considers diagonal movement as well as straight lines.",
        "long_description": [
            "The Diagonal heuristic improves on the Manhattan heuristic by considering diagonal movement in addition to horizontal and vertical moves. It is especially useful for grid-based pathfinding when diagonal movement is allowed."
        ],
        "type": "Heuristic Function",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)",
        "common_applications": ["Diagonal movement in grid-based games", "3D navigation", "Robotics"]
    },
    "Dijkstra": {
        "title": "Dijkstra's Algorithm",
        "short_description": "Finds the shortest path by exploring all nodes evenly.",
        "long_description": [
            "Dijkstra's algorithm explores all possible paths in the grid evenly, guaranteeing the shortest path. It works well in grids where movement cost is uniform, though it can be slower than A* when heuristics are not used."
        ],
        "type": "Pathfinding Algorithm",
        "time_complexity": "O(n^2), or O(n log n) with a priority queue",
        "space_complexity": "O(n)",
        "common_applications": ["Network routing", "Mapping software", "Traffic navigation"]
    },
    "Recursive DFS": {
        "title": "Recursive Depth-First Search (DFS)",
        "short_description": "Creates mazes by recursively carving paths through the grid.",
        "long_description": [
            "Recursive DFS generates mazes by recursively dividing the grid and carving paths between sections. The resulting mazes have a tree-like structure without loops, ensuring that every area of the maze is reachable from the start."
        ],
        "type": "Maze Generation Algorithm",
        "time_complexity": "O(n), where n is the number of cells",
        "space_complexity": "O(n)",
        "common_applications": ["Maze generation", "Puzzle games"]
    },
    "Growing Tree": {
        "title": "Growing Tree",
        "short_description": "Randomly selects cells to grow a maze, creating diverse patterns.",
        "long_description": [
            "The Growing Tree algorithm generates mazes by randomly selecting cells from a list and carving paths to neighboring cells. Each cell that is carved adds new potential paths to explore, resulting in diverse maze structures.",
            "This method allows for both simple, structured mazes and more complex, winding paths depending on how cells are selected."
        ],
        "type": "Maze Generation Algorithm",
        "time_complexity": "O(n), where n is the number of cells",
        "space_complexity": "O(n)",
        "common_applications": ["Maze generation", "Puzzle games"]
    },
    "Binary Tree": {
        "title": "Binary Tree",
        "short_description": "Generates mazes using a binary tree structure.",
        "long_description": [
            "Binary Tree is a simple and efficient maze generation algorithm that divides the grid into sections using a binary tree pattern. This results in mazes with long, straight corridors and relatively simple paths."
        ],
        "type": "Maze Generation Algorithm",
        "time_complexity": "O(n), where n is the number of cells",
        "space_complexity": "O(n)",
        "common_applications": ["Maze generation", "Procedural content generation"]
    },
    "Sidewinder": {
        "title": "Sidewinder",
        "short_description": "Generates mazes row by row, favoring horizontal paths.",
        "long_description": [
            "Sidewinder is a variation of the Binary Tree algorithm, generating mazes by carving paths row by row, leading to a maze structure with long horizontal corridors and shorter vertical ones."
        ],
        "type": "Maze Generation Algorithm",
        "time_complexity": "O(n), where n is the number of cells",
        "space_complexity": "O(n)",
        "common_applications": ["Maze generation", "Puzzle games"]
    },
    "Custom": {
        "title": "Custom Maze Setup",
        "short_description": "Manually place start, end, and barriers to customize the maze.",
        "long_description": [
            "The custom maze setup allows the user to manually place the start and end points, and build barriers to create a custom maze layout. This flexibility is ideal for testing different algorithms or creating specific scenarios."
        ],
        "type": "Maze Generation Algorithm",
        "time_complexity": "N/A",
        "space_complexity": "N/A",
        "common_applications": ["Custom pathfinding tests", "User-defined layouts"]
    },
    "Bubble Sort": {
        "title": "Bubble Sort",
        "short_description": "A simple algorithm that repeatedly swaps adjacent elements if they are in the wrong order.",
        "long_description": [
            "Bubble Sort is a basic sorting algorithm that compares adjacent elements and swaps them if they are out of order. This process repeats until the entire array is sorted.",
            "Though easy to understand and implement, Bubble Sort is inefficient on large datasets due to its O(n^2) time complexity in the worst case."
        ],
        "type": "Sorting Algorithm",
        "time_complexity": "Best: O(n), Average: O(n^2), Worst: O(n^2)",
        "space_complexity": "O(1)",
        "common_applications": ["Teaching sorting algorithms"]
    },
    "Insertion Sort": {
        "title": "Insertion Sort",
        "short_description": "Builds the sorted array one element at a time by inserting elements into their correct position.",
        "long_description": [
            "Insertion Sort works by taking one element at a time and inserting it into its correct position in a sorted part of the array. It's more efficient than Bubble Sort for small arrays and partially sorted data.",
            "Though it's O(n^2) in the worst case, Insertion Sort performs well on small or nearly sorted datasets."
        ],
        "type": "Sorting Algorithm",
        "time_complexity": "Best: O(n), Average: O(n^2), Worst: O(n^2)",
        "space_complexity": "O(1)",
        "common_applications": ["Small datasets", "Partially sorted data"]
    },
    "Selection Sort": {
        "title": "Selection Sort",
        "short_description": "A simple comparison-based algorithm that repeatedly selects the smallest element.",
        "long_description": [
            "Selection Sort divides the array into a sorted and an unsorted region. It repeatedly selects the smallest (or largest, depending on sorting order) element from the unsorted part and swaps it with the first unsorted element.",
            "It has a consistent O(n^2) time complexity regardless of the data's initial order."
        ],
        "type": "Sorting Algorithm",
        "time_complexity": "Best: O(n^2), Average: O(n^2), Worst: O(n^2)",
        "space_complexity": "O(1)",
        "common_applications": ["Teaching sorting algorithms"]
    },
    "Cocktail Shaker Sort": {
        "title": "Cocktail Shaker Sort",
        "short_description": "A bi-directional variation of Bubble Sort that sorts in both directions each pass.",
        "long_description": [
            "Cocktail Shaker Sort, also known as bidirectional Bubble Sort, sorts the array in both directions in each pass through the list. It improves upon Bubble Sort by slightly reducing the number of passes needed.",
            "However, its time complexity remains O(n^2), making it inefficient for large datasets."
        ],
        "type": "Sorting Algorithm",
        "time_complexity": "Best: O(n), Average: O(n^2), Worst: O(n^2)",
        "space_complexity": "O(1)",
        "common_applications": ["Teaching sorting algorithms"]
    },
    "Comb Sort": {
        "title": "Comb Sort",
        "short_description": "An improved version of Bubble Sort that eliminates turtles (small values at the end of the list).",
        "long_description": [
            "Comb Sort improves on Bubble Sort by using a gap that decreases over time, instead of always comparing adjacent elements. This helps to move small elements (turtles) more quickly to their correct position.",
            "It performs better than Bubble Sort, especially for medium-sized datasets."
        ],
        "type": "Sorting Algorithm",
        "time_complexity": "Best: O(n log n), Average: O(n^2/log n), Worst: O(n^2)",
        "space_complexity": "O(1)",
        "common_applications": ["Teaching sorting algorithms", "Improving on Bubble Sort"]
    },
    "Shell Sort": {
        "title": "Shell Sort",
        "short_description": "A generalization of Insertion Sort that allows the exchange of far-apart elements.",
        "long_description": [
            "Shell Sort improves on Insertion Sort by allowing the exchange of far-apart elements. It sorts elements at specific gap intervals and reduces the gap with each pass, making the data more sorted for the final Insertion Sort.",
            "The performance depends on the gap sequence, but it generally performs better than O(n^2) algorithms."
        ],
        "type": "Sorting Algorithm",
        "time_complexity": "Best: O(n log n), Average: O(n^(3/2)), Worst: O(n^2)",
        "space_complexity": "O(1)",
        "common_applications": ["Partially sorted data", "Improving Insertion Sort"]
    },
    "Merge Sort": {
        "title": "Merge Sort",
        "short_description": "A divide-and-conquer algorithm that splits the array and merges sorted subarrays.",
        "long_description": [
            "Merge Sort is a stable, comparison-based, divide-and-conquer algorithm. It works by recursively splitting the array into smaller subarrays and merging them in sorted order.",
            "Merge Sort guarantees O(n log n) time complexity for all cases, making it highly efficient for large datasets."
        ],
        "type": "Sorting Algorithm",
        "time_complexity": "Best: O(n log n), Average: O(n log n), Worst: O(n log n)",
        "space_complexity": "O(n)",
        "common_applications": ["Large datasets", "Stable sorting"]
    },
    "Quick Sort": {
        "title": "Quick Sort",
        "short_description": "A fast divide-and-conquer algorithm that selects a pivot and partitions the array.",
        "long_description": [
            "Quick Sort is a highly efficient sorting algorithm that selects a pivot element and partitions the array into two subarrays: elements smaller than the pivot and elements greater than the pivot. It then recursively sorts the subarrays.",
            "Although its worst-case time complexity is O(n^2), this can be avoided with good pivot selection strategies."
        ],
        "type": "Sorting Algorithm",
        "time_complexity": "Best: O(n log n), Average: O(n log n), Worst: O(n^2)",
        "space_complexity": "O(log n)",
        "common_applications": ["Large datasets", "General-purpose sorting"]
    },
    "Tim Sort": {
        "title": "Tim Sort",
        "short_description": "A hybrid sorting algorithm derived from Merge Sort and Insertion Sort.",
        "long_description": [
            "Tim Sort is a hybrid sorting algorithm that combines the best of Merge Sort and Insertion Sort. It divides the array into small chunks (runs), sorts the runs using Insertion Sort, and then merges them using a modified Merge Sort.",
            "Tim Sort is optimized for real-world data and is used in Python’s built-in sort() and Java's Arrays.sort() methods."
        ],
        "type": "Sorting Algorithm",
        "time_complexity": "Best: O(n), Average: O(n log n), Worst: O(n log n)",
        "space_complexity": "O(n)",
        "common_applications": ["Real-world datasets", "Python and Java sorting", "General-purpose sorting"]
    },
    "Heap Sort": {
        "title": "Heap Sort",
        "short_description": "A comparison-based sorting algorithm that uses a binary heap structure.",
        "long_description": [
            "Heap Sort works by building a max heap from the input data and repeatedly extracting the maximum element to build a sorted array. It is efficient, with a guaranteed O(n log n) time complexity.",
            "Though not a stable sort, Heap Sort is useful when memory space is a concern, as it sorts in place."
        ],
        "type": "Sorting Algorithm",
        "time_complexity": "Best: O(n log n), Average: O(n log n), Worst: O(n log n)",
        "space_complexity": "O(1)",
        "common_applications": ["Memory-constrained environments", "General-purpose", "In-place sorting"]
    },
    "Tree Sort": {
        "title": "Tree Sort",
        "short_description": "A sorting algorithm that builds a binary search tree from the array elements.",
        "long_description": [
            "Tree Sort works by inserting all elements into a binary search tree (BST) and performing an in-order traversal to extract the elements in sorted order. Its performance depends on the balance of the tree.",
            "In the average case, Tree Sort is O(n log n), but in the worst case, it can degrade to O(n^2) if the tree becomes unbalanced."
        ],
        "type": "Sorting Algorithm",
        "time_complexity": "Best: O(n log n), Average: O(n log n), Worst: O(n^2)",
        "space_complexity": "O(n)",
        "common_applications": ["Datasets with tree structures", "In-order traversal", "Small to medium datasets"]
    },
    "Bogo Sort": {
        "title": "Bogo Sort",
        "short_description": "A highly inefficient sorting algorithm that randomly shuffles the array until sorted.",
        "long_description": [
            "Bogo Sort works by generating random permutations of the input array until it happens to be sorted. It is considered a joke algorithm due to its inefficiency and impracticality for real-world use.",
            "Its average-case time complexity is O(n!) due to the random shuffling, making it one of the least efficient sorting algorithms."
        ],
        "type": "Sorting Algorithm",
        "time_complexity": "Best: O(1), Average: O((n+1)!), Worst: O(∞)",
        "space_complexity": "O(1)",
        "common_applications": ["Teaching algorithm inefficiency", "Demonstration of brute force"]
    }
}
