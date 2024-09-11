from .draw_utils import *
import random

def bubble_sort(lst, visualization, persistent_colors, ascending=True):
    """
    Bubble Sort with detailed visualization and early exit optimization.
    This algorithm compares adjacent elements and swaps them if they are in the wrong order,
    effectively "bubbling" the largest (or smallest) element to its correct position on each pass.
    The process is repeated until the list is fully sorted or no swaps are made in a pass.
    
    Visualization Details:
    - Elements being compared are highlighted in red.
    - After a swap (if needed), the swapped elements remain highlighted in red.
    - Once an element reaches its correct position, it is highlighted in green.
    - The final pass turns all elements green one by one to indicate the list is fully sorted.

    Big O Notations:
    - Time Complexity: 
      - Best Case: O(n) when the list is already sorted (due to the early exit optimization).
      - Average Case: O(n^2) as it requires two nested loops for most cases.
      - Worst Case: O(n^2) when the list is sorted in reverse order.
    - Space Complexity: O(1), as it only requires a constant amount of additional space.
    
    Arguments:
    lst -- the list to be sorted.
    visualization -- the visualization object to handle drawing.
    persistent_colors -- a dictionary to track the colors of each element in the visualization.
    ascending -- whether to sort the list in ascending order (default is True).
    
    Returns:
    Yields comparisons, array_accesses, and swaps for each step of the visualization.
    """
    
    comparisons = 0
    array_accesses = 0
    swaps = 0

    n = len(lst)
    last_sorted_index = None

    for i in range(n - 1):
        swapped = False # Initialize the swapped flag for each pass

        for j in range(n - 1 - i):

            comparisons += 1  # Every comparison in the if condition is a comparison

            num1 = lst[j]
            num2 = lst[j + 1]
            array_accesses += 2  # Accessing lst[j] and lst[j+1] counts as 2 accesses

            # Highlight the two elements being compared
            persistent_colors[j] = visualization.COMPARISON_COLOR
            persistent_colors[j + 1] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
            yield comparisons, array_accesses, swaps

            # Swap the two elements if they are in the wrong order
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                array_accesses += 4  # Swapping involves 4 accesses (2 reads, 2 writes)
                swaps += 1  # Count the swap

                swapped = True  # Mark that a swap has occurred

                # Highlight the swapped elements
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
                yield comparisons, array_accesses, swaps

            # Revert the compared elements back to their default color
            persistent_colors[j] = visualization.BAR_COLOR
            persistent_colors[j + 1] = visualization.BAR_COLOR

        # Mark the last element of the current pass as sorted
        if last_sorted_index is not None:
            persistent_colors[last_sorted_index] = visualization.BAR_COLOR  # Revert the previous sorted element to grey
        persistent_colors[n - 1 - i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
        yield comparisons, array_accesses, swaps

        last_sorted_index = n - 1 - i

        # If no swaps were made, the list is sorted, and we can exit early
        if not swapped:
            persistent_colors[last_sorted_index] = visualization.BAR_COLOR # Reset last sorted element to grey
            break

    # Final pass to mark all elements as fully sorted by turning them green
    for i in range(n):
        persistent_colors[i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
        yield comparisons, array_accesses, swaps

def insertion_sort(lst, visualization, persistent_colors, ascending=True):
    """
    Insertion Sort with detailed visualization.
    This algorithm shifts elements to their correct positions, 
    making space for the current element being sorted.

    Visualization Details:
    - The current element being sorted is highlighted in red.
    - Elements being compared and shifted are also highlighted in red.
    - Once an element is placed in its correct position, it is highlighted in green.
    - The final pass turns all elements green one by one to indicate the list is fully sorted.

    Big O Notations:
    - Time Complexity: 
      - Best Case: O(n) when the list is already sorted.
      - Average Case: O(n^2) due to the nested loop where each element is compared with every other element.
      - Worst Case: O(n^2) when the list is sorted in reverse order.
    - Space Complexity: O(1), as it only requires a constant amount of additional space.

     Note:
    - Another visualization method (seen in insertion_sort_swaps below) could use swaps instead of shifts to show how an element 
      is inserted into its correct position, but this would result in inaccurate counts of comparisons and array accesses, as swaps involve more operations.
    
    Arguments:
    lst -- the list to be sorted.
    visualization -- the visualization object to handle drawing.
    persistent_colors -- a dictionary to track the colors of each element in the visualization.
    ascending -- whether to sort the list in ascending order (default is True).

    Returns:
    Yields comparisons and array_accesses for each step of the visualization.
    """
    
    comparisons = 0
    array_accesses = 0

    n = len(lst)
    last_sorted_index = None

    for i in range(1, n):
        j = i
        current_value = lst[i]

        array_accesses += 2  # Accessing lst[i] (current_value) and lst[j - 1] (while loop)
        comparisons += 1 # Each iteration of the while loop performs a comparison

        # Highlight the previous and current element in red as we start to find its correct position
        persistent_colors[i - 1] = visualization.COMPARISON_COLOR
        persistent_colors[i] = visualization.COMPARISON_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

        # Shift elements that are greater/less (based on order) than the current element
        while j > 0 and ((lst[j - 1] > current_value and ascending) or (lst[j - 1] < current_value and not ascending)):
            comparisons += 1 # Comparison in the next iteration
            array_accesses += 1  # Accessing lst[j - 1] next iteration

            # Shift the previous element one position to the right to make room for the current element
            lst[j] = lst[j - 1]
            array_accesses += 2 # Accessing lst[j-1] and assigning to lst[j]

            # Highlight the two elements being shifted in red
            persistent_colors[j - 1] = visualization.COMPARISON_COLOR
            persistent_colors[j] = visualization.COMPARISON_COLOR
        
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses 

            # Revert the previously highlighted elements to grey before moving on
            persistent_colors[j] = visualization.BAR_COLOR
            persistent_colors[j - 1] = visualization.BAR_COLOR

            if last_sorted_index is not None:
                persistent_colors[last_sorted_index] = visualization.SORTED_COLOR  # Revert to green if overwritten


            j -= 1

        # Place the current element in its correct position
        lst[j] = current_value
        array_accesses += 1 # Assigning current_value to lst[j]

        if last_sorted_index is not None:
            persistent_colors[last_sorted_index] = visualization.BAR_COLOR  # Revert the previous sorted element to grey
        
        # Mark the placed element as green to indicate it's in the correct position
        if i == j:
            # Special case: If the current element was already in the correct position, 
            # mark the previous element as sorted (green) and revert the current element to grey
            persistent_colors[j - 1] = visualization.SORTED_COLOR
            persistent_colors[j] = visualization.BAR_COLOR
            last_sorted_index = j - 1
        else:
            # Regular case: Mark the current element as sorted (green)
            persistent_colors[j] = visualization.SORTED_COLOR
            last_sorted_index = j

        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

    persistent_colors[last_sorted_index] = visualization.BAR_COLOR # Reset last sorted element to grey
    persistent_colors[i] = visualization.SORTED_COLOR
    draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
    yield comparisons, array_accesses

    persistent_colors[i] = visualization.BAR_COLOR # Reset last sorted element to grey

    # Final pass to mark all elements as fully sorted by turning them green
    for i in range(n):
        persistent_colors[i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

def selection_sort(lst, visualization, persistent_colors, ascending=True):
    """
    Selection Sort with detailed visualization.
    This algorithm selects the smallest (or largest) element from the unsorted portion 
    of the list and swaps it with the first unsorted element, gradually building a 
    sorted portion at the beginning of the list.

    Visualization Details:
    - The current minimum element is highlighted in blue, and any new minimum found is highlighted in yellow.
    - Elements being compared are highlighted in red.
    - Once an element is placed in its correct position, it is highlighted in green.
    - The final pass turns all elements green one by one to indicate the list is fully sorted.

    Big O Notations:
    - Time Complexity: 
        - Best Case: O(n^2) as it always performs the same number of comparisons regardless of the list order.
        - Average Case: O(n^2) due to the nested loop where each element is compared with every other element.
        - Worst Case: O(n^2) when the list is sorted in reverse order.
    - Space Complexity: O(1), as it only requires a constant amount of additional space.
        
    Arguments:
    lst -- the list to be sorted.
    visualization -- the visualization object to handle drawing.
    persistent_colors -- a dictionary to track the colors of each element in the visualization.
    ascending -- whether to sort the list in ascending order (default is True).
    
    Returns:
    Yields comparisons, array_accesses, and swaps for each step of the visualization.
    """
    comparisons = 0
    array_accesses = 0
    swaps = 0

    n = len(lst)
    last_sorted_index = None

    for i in range(n - 1):
        initial_index = i
        min_index = i
        persistent_colors[initial_index] = visualization.SECONDARY_ACTIVE_COLOR # Highlight initial minimum in blue

        for j in range(i + 1, n):
            comparisons += 1 # # Comparison between lst[j] and lst[min_index]
            array_accesses += 2 # Accessing lst[j] and lst[min_index] for comparison

            # Highlight the elements being compared in red
            persistent_colors[j] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
            yield comparisons, array_accesses, swaps  # Yield after highlighting comparison

            # If a new minimum is found, update the minimum index and colors
            if (lst[j] < lst[min_index] and ascending) or (lst[j] > lst[min_index] and not ascending):
                if min_index != initial_index:  # Revert the previous minimum to grey if it wasn't the initial index
                    persistent_colors[min_index] = visualization.BAR_COLOR
                min_index = j
                persistent_colors[min_index] = visualization.PRIMARY_ACTIVE_COLOR # New minimum is highlighted in yellow

                # Update the visualization to reflect the new minimum
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
                yield comparisons, array_accesses, swaps 

            # Revert the compared element to grey after the comparison
            if j != min_index:  # Ensure the current minimum stays yellow
                persistent_colors[j] = visualization.BAR_COLOR

        if min_index != i:
            # Swap the elements to place the new minimum in the correct position
            lst[i], lst[min_index] = lst[min_index], lst[i]
            array_accesses += 4  # Each swap involves 2 reads and 2 writes
            swaps += 1

        # Mark the element just placed in its correct position as green
        if last_sorted_index is not None:
            persistent_colors[last_sorted_index] = visualization.BAR_COLOR  # Revert the previous sorted element to grey
        persistent_colors[min_index] = visualization.BAR_COLOR
        persistent_colors[i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
        yield comparisons, array_accesses, swaps

        last_sorted_index = i

    persistent_colors[last_sorted_index] = visualization.BAR_COLOR # Reset last sorted element to grey
    persistent_colors[i + 1] = visualization.SORTED_COLOR
    draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
    yield comparisons, array_accesses, swaps

    persistent_colors[i + 1] = visualization.BAR_COLOR # Reset last sorted element to grey

    # Final pass to mark all elements as fully sorted by turning them green
    for i in range(n):
        persistent_colors[i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
        yield comparisons, array_accesses, swaps

def merge_sort(lst, visualization, persistent_colors=None, ascending=True, left=0, right=None, comparisons=0, array_accesses=0):
    """
    Merge sort with detailed visualization.

    This function implements the merge sort algorithm, an out-of-place divide-and-conquer sorting technique. 
    The algorithm splits the list into subarrays, recursively sorts them, and then merges them back together. 
    During the merging process, a current_valueorary array is used to store the merged elements, which simplifies 
    the merging logic and allows for accurate visualization of the sorting steps.

    Visualization Details:
    - The left and right boundaries of the current subarray are highlighted in blue.
    - The middle element, representing the division point, is highlighted in yellow.
    - During the merging process, the elements being compared are highlighted in red.
    - Elements that are placed in their correct position during the merge are highlighted in green.
    - All elements are finally marked green when the entire array is sorted.

    Big O Notations:
    - Time Complexity: 
        - Best Case: O(n log n), because merge sort always divides the list and merges it, regardless of its initial order.
        - Average Case: O(n log n), as the list is always divided and merged, leading to consistent performance.
        - Worst Case: O(n log n), even in the worst case, merge sort always splits and merges the list, maintaining O(n log n) complexity.
    - Space Complexity: O(n), due to the additional space required to store the temporary array for merging.

    Arguments:
    - lst: The list to be sorted.
    - visualization: The visualization object responsible for rendering the sorting process.
    - persistent_colors: A dictionary tracking the colors of each element in the visualization.
    - ascending: Whether to sort the list in ascending order (default is True).
    - left: The starting index of the subarray (default is 0).
    - right: The ending index of the subarray (default is None, which means the full array).
    - comparisons: The running total of comparisons made so far.
    - array_accesses: The running total of array accesses made so far.

    Yields:
    - comparisons: The updated number of comparisons after each significant step.
    - array_accesses: The updated number of array accesses after each significant step.
    
    Returns:
    - The final counts of comparisons and array accesses after the sorting is complete.
    """

    # Set 'right' to the last index of the list if not provided.
    if right is None:
        right = len(lst) - 1

    # Reset all element colors to grey.
    persistent_colors = {index: visualization.BAR_COLOR for index in range(len(lst))}

    # Base case: If the subarray has only one element, it's already sorted.
    if left == right:
        # Highlight the single element to indicate it's the boundary of a subarray.
        persistent_colors[left] = visualization.SECONDARY_ACTIVE_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

        # Revert the element color back to grey after processing.
        persistent_colors[left] = visualization.BAR_COLOR
        return comparisons, array_accesses

    # Divide the array only if there are two or more elements to sort
    if left < right:
        mid = (left + right) // 2

        # Highlight the left, right, and middle elements to show the current subarray being processed
        persistent_colors[left] = visualization.SECONDARY_ACTIVE_COLOR  
        persistent_colors[right] = visualization.SECONDARY_ACTIVE_COLOR 
        persistent_colors[mid] = visualization.PRIMARY_ACTIVE_COLOR 
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

        # Recursively sort the left and right halves
        comparisons, array_accesses = yield from merge_sort(
            lst, visualization, persistent_colors, ascending, left, mid, comparisons, array_accesses
        )
        comparisons, array_accesses = yield from merge_sort(
            lst, visualization, persistent_colors, ascending, mid + 1, right, comparisons, array_accesses
        )

        # Prepare a temporary array to store the merged elements
        temp = []

        i = left
        j = mid + 1

        # Merge the elements from the left and right halves into the temporary array.
        while i <= mid and j <= right:
            comparisons += 1 # Comparing lst[i] and lst[j
            array_accesses += 2  # Accessing elements from the left and right subarrays lst[i] and lst[j]

            # Highlight the left and right boundaries during the merge process.
            persistent_colors[left] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[right] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[mid] = visualization.PRIMARY_ACTIVE_COLOR 

            if (lst[i] <= lst[j] and ascending) or (lst[i] >= lst[j] and not ascending):
                temp.append(lst[i])
                array_accesses += 1  # Increment for accessing lst[i] to copy to temp

                # Highlight the element being merged in red.
                persistent_colors[i] = visualization.COMPARISON_COLOR
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
                yield comparisons, array_accesses

                # Revert the element color after it is processed.
                persistent_colors[i] = visualization.BAR_COLOR

                i += 1
            else:
                temp.append(lst[j])
                array_accesses += 1 # Accessing lst[i] to append it to temp

                # Highlight the element being merged in red.
                persistent_colors[j] = visualization.COMPARISON_COLOR
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
                yield comparisons, array_accesses

                # Revert the element color after it is processed.
                persistent_colors[j] = visualization.BAR_COLOR

                j += 1

        # Add any remaining elements from the left subarray to the temp array.
        while i <= mid:
            array_accesses += 1 # Accessing lst[i] to append it to temp
            temp.append(lst[i])

            # Ensure left and right boundaries are highlighted during the merge
            persistent_colors[left] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[right] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[mid] = visualization.PRIMARY_ACTIVE_COLOR 

            # Highlight the element being merged in red.
            persistent_colors[i] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            # Revert the element color after it is processed.
            persistent_colors[i] = visualization.BAR_COLOR
            i += 1


        # Add any remaining elements from the right subarray
        while j <= right:
            array_accesses += 1 # Accessing lst[i] to append it to temp
            temp.append(lst[j])

            # Ensure left and right boundaries are highlighted during the merge
            persistent_colors[left] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[right] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[mid] = visualization.PRIMARY_ACTIVE_COLOR 

            # Highlight the element being merged in red.
            persistent_colors[j] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            # Revert the element color after it is processed.
            persistent_colors[j] = visualization.BAR_COLOR
            j += 1

        # Copy the sorted elements from the temporary array back to the original array
        for k in range(len(temp)):
            lst[left + k] = temp[k]
            array_accesses += 2  # Accessing lst[left + k] and temp[k]

            # Ensure left and right boundaries are highlighted during the merge
            persistent_colors[left] = visualization.BAR_COLOR
            persistent_colors[right] = visualization.BAR_COLOR
            persistent_colors[mid] = visualization.BAR_COLOR 
            persistent_colors[left + k] = visualization.SORTED_COLOR

            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            # Revert the color after visualization.
            persistent_colors[left + k] = visualization.BAR_COLOR 

    # Final pass to mark all elements as sorted (green) one by one
    if left == 0 and right == len(lst) - 1:  # Only perform this when the full array is sorted
        for i in range(len(lst)):
            persistent_colors[i] = visualization.SORTED_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

    return comparisons, array_accesses

def quick_sort(lst, visualization, persistent_colors=None, ascending=True, left=0, right=None, comparisons=0, array_accesses=0):
    """
    Quick sort with detailed visualization.

    This function implements the quick sort algorithm, a divide-and-conquer sorting technique that selects
    a pivot element, partitions the list into elements less than and greater than the pivot, and then 
    recursively sorts the subarrays. The function visualizes each step, highlighting the pivot, comparisons, 
    and swaps, and tracks the sorting progress by counting comparisons and array accesses.

    Visualization Details:
    - The pivot element is highlighted in yellow.
    - Elements being compared are highlighted in red.
    - Swapped elements are highlighted in green.
    - The left and right boundaries are highlighted in blue.
    - All elements are finally marked green when the entire array is sorted.

    Big O Notations:
    - Time Complexity:
        - Best Case: O(n log n), occurs when the pivot divides the array into two nearly equal halves consistently.
        - Average Case: O(n log n), typical case where the pivot division is balanced on average.
        - Worst Case: O(n^2), occurs when the pivot selection consistently leads to the most unbalanced partitions (e.g., sorted arrays).
    - Space Complexity: O(log n) for the recursive stack space, as Quick Sort can be implemented in-place.

    Arguments:
    - lst: The list to be sorted.
    - visualization: The visualization object responsible for rendering the sorting process.
    - persistent_colors: A dictionary tracking the colors of each element in the visualization.
    - ascending: Whether to sort the list in ascending order (default is True).
    - left: The starting index of the subarray (default is 0).
    - right: The ending index of the subarray (default is None, which means the full array).
    - comparisons: The running total of comparisons made so far.
    - array_accesses: The running total of array accesses made so far.

    Yields:
    - comparisons: The updated number of comparisons after each significant step.
    - array_accesses: The updated number of array accesses after each significant step.
    
    Returns:
    - The final counts of comparisons and array accesses after the sorting is complete.
    """

    if right is None:
        right = len(lst) - 1

    # Only proceed if the subarray has more than one element
    if left < right:
        # Initialize boundaries and the pivot
        i = left
        j = right - 1
        pivot_index = random.randint(left, right)

        # Highlight the pivot before swapping
        persistent_colors[pivot_index] = visualization.PRIMARY_ACTIVE_COLOR
        persistent_colors[right] = visualization.COMPARISON_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

        # Swap the random pivot with the last element
        lst[pivot_index], lst[right] = lst[right], lst[pivot_index]
        array_accesses += 4  # Accessing and swapping the pivot

        # Visualize the swap
        persistent_colors[pivot_index] = visualization.COMPARISON_COLOR
        persistent_colors[right] = visualization.PRIMARY_ACTIVE_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

        # Revert the swapped elements to their default color
        persistent_colors[pivot_index] = visualization.BAR_COLOR

        pivot_index = right
        pivot_value = lst[pivot_index]
        array_accesses += 1

        # Highlight the pivot and the left and right boundaries
        persistent_colors[left] = visualization.SECONDARY_ACTIVE_COLOR
        persistent_colors[right - 1] = visualization.SECONDARY_ACTIVE_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

        swapped = False  # Flag used for avoiding double rendering

        # Partitioning process
        while i < j:

            comparisons += 1 # Comparing lst[i] and pivot_value
            array_accesses += 1  # Accessing lst[i] (pivot_value not counted as already in variable)

            persistent_colors[i] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            # Move the left pointer to the right until an element greater/less than the pivot is found
            while i < right and ((lst[i] < pivot_value and ascending) or (lst[i] > pivot_value and not ascending)):

                comparisons += 1 # Comparison for next iteration
                array_accesses += 1  # Accessing lst[i] for next iteration

                # Revert the color of the current element
                persistent_colors[i] = visualization.BAR_COLOR

                if i == left:
                    persistent_colors[left] = visualization.SECONDARY_ACTIVE_COLOR
                
                i += 1

                # Highlight the new position of the left pointer
                persistent_colors[i] = visualization.COMPARISON_COLOR
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
                yield comparisons, array_accesses


            comparisons += 1 # Comparing lst[j] and pivot_value
            array_accesses += 1  # Accessing lst[j] (pivot_value not counted as already in variable)

            # Avoids double rendering step for j when elements swapped succesfully and avoid i and j crossing ovew
            if swapped and i < j:
                j -= 1
                swapped = False

            persistent_colors[j] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            # Move the right pointer to the left until an element less/greater than the pivot is found
            while j > left and ((lst[j] >= pivot_value and ascending) or (lst[j] <= pivot_value and not ascending)) and j != i:

                comparisons += 1 # Comparison for next iteration
                array_accesses += 1  # Accessing lst[j] for next iteration

                # Revert the color of the current element
                persistent_colors[j] = visualization.BAR_COLOR

                if j == right - 1:
                    persistent_colors[right - 1] = visualization.SECONDARY_ACTIVE_COLOR

                j -= 1

                # Highlight the new position of the right pointer
                persistent_colors[j] = visualization.COMPARISON_COLOR
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
                yield comparisons, array_accesses

            # Swap elements if left pointer is still less than right pointer
            if i < j:
                array_accesses += 4  # 2 reads, 2 writes for the swap
                lst[i], lst[j] = lst[j], lst[i]

                # Highlight the swapped elements
                persistent_colors[i] = visualization.SORTED_COLOR
                persistent_colors[j] = visualization.SORTED_COLOR
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
                yield comparisons, array_accesses

                # Revert the swapped elements to their default color
                persistent_colors[i] = visualization.BAR_COLOR
                persistent_colors[j] = visualization.BAR_COLOR

                persistent_colors[left] = visualization.SECONDARY_ACTIVE_COLOR
                persistent_colors[right - 1] = visualization.SECONDARY_ACTIVE_COLOR

                i += 1 # Avoids double rendering step for i when elements swapped succesfully
                swapped = True # Flag used for avoiding double rendering step for j

        comparisons += 1 # Comparing lst[i] and pivot value
        array_accesses += 1 # Accessing lst[i] for next iteration

        # Final swap to place the pivot in its correct position
        if (ascending and lst[i] > pivot_value) or (not ascending and lst[i] < pivot_value):
            array_accesses += 4  # 2 reads, 2 writes for the swap
            lst[i], lst[pivot_index] = lst[pivot_index], lst[i]

            # Highlight the pivot's new position
            persistent_colors[i] = visualization.SORTED_COLOR
            persistent_colors[pivot_index] = visualization.PRIMARY_ACTIVE_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            # Revert the swapped elements to their default color
            persistent_colors[i] = visualization.BAR_COLOR
            persistent_colors[pivot_index] = visualization.BAR_COLOR
        else:
            persistent_colors[left] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[right - 1] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[pivot_index] = visualization.SORTED_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            persistent_colors[pivot_index] = visualization.BAR_COLOR

        # Revert the pivot and pointers back to their default color
        persistent_colors[i] = visualization.BAR_COLOR
        persistent_colors[j] = visualization.BAR_COLOR
        persistent_colors[left] = visualization.BAR_COLOR
        persistent_colors[right - 1] = visualization.BAR_COLOR
        persistent_colors[pivot_index] = visualization.BAR_COLOR

        # Recursive calls to sort the subarrays
        comparisons, array_accesses = yield from quick_sort(lst, visualization, persistent_colors, ascending, left, i - 1, comparisons, array_accesses)
        comparisons, array_accesses = yield from quick_sort(lst, visualization, persistent_colors, ascending, i + 1, right, comparisons, array_accesses)

    # Final pass to mark all elements as sorted
    if left == 0 and right == len(lst) - 1:
        for i in range(len(lst)):
            persistent_colors[i] = visualization.SORTED_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

    return comparisons, array_accesses

def heap_sort(lst, visualization, persistent_colors=None, ascending=True, comparisons=0, array_accesses=0):
    """
    Performs Heap Sort with detailed visualization, including color depth for heap levels.

    Heap Sort is a comparison-based sorting algorithm that utilizes a binary heap data structure. 
    The algorithm builds a max heap (for ascending sort) and repeatedly swaps the root (largest element) 
    with the last element, then reduces the heap size and re-heapifies the root. 
    This implementation includes visualization steps to highlight comparisons and swaps, 
    and uses color coding to indicate the depth of elements in the binary heap.

    Visualization Details:
    - Elements being compared are highlighted in red.
    - Swapped elements are highlighted in red.
    - Depth levels are indicated by varying colors.
    - Once an element is placed in its correct position, it is highlighted in green.
    - The final pass turns all elements green one by one to indicate the list is fully sorted.

    Big O Notations:
    - Time Complexity:
    - Best Case: O(n log n), occurs consistently as heap sort always follows the same process.
    - Average Case: O(n log n), typical case for the majority of inputs.
    - Worst Case: O(n log n), heap sort's time complexity is unaffected by the initial order of the elements.
    - Space Complexity: O(1) for the iterative version since the heap is built in-place without requiring extra space.

    Arguments:
    - lst: The list of elements to be sorted.
    - visualization: The visualization object responsible for rendering the sorting process.
    - persistent_colors: A dictionary tracking the colors of each element in the visualization.
    - ascending: Boolean indicating whether to sort in ascending (True) or descending (False) order.
    - comparisons: Running total of comparisons made so far.
    - array_accesses: Running total of array accesses made so far.

    Yields:
    - comparisons: The updated number of comparisons after each significant step.
    - array_accesses: The updated number of array accesses after each significant step.

    Returns:
    - The final counts of comparisons and array accesses after the sorting is complete.
    """


    def calculate_depth(index):
        """Calculates the depth of a node in a binary heap given its index."""
        depth = 0
        while index > 0:
            index = (index - 1) // 2
            depth += 1
        return depth

    def heapify(lst, n, i):
        """
        Iterative heapify function to maintain max heap property.
        """

        nonlocal comparisons, array_accesses
        current_root_index = i

        while True:
            left_child_index = 2 * current_root_index + 1
            right_child_index = 2 * current_root_index + 2
            depth = calculate_depth(current_root_index)

            # Assume current root is the largest initially
            largest_index = current_root_index

            # Compare the root with its left child (if exists)
            if left_child_index < n:
                comparisons += 1
                array_accesses += 2  # Accessing lst[left_child_index] and lst[largest_index]

                # Highlight the comparison
                persistent_colors[current_root_index] = visualization.COMPARISON_COLOR
                persistent_colors[left_child_index] = visualization.COMPARISON_COLOR
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
                yield comparisons, array_accesses

                if (lst[left_child_index] > lst[largest_index] if ascending else lst[left_child_index] < lst[largest_index]):
                    largest_index = left_child_index

                # Revert to depth color after comparison
                persistent_colors[current_root_index] = visualization.get_color_for_depth(depth)
                persistent_colors[left_child_index] = visualization.get_color_for_depth(depth + 1)

            # Compare the largest so far with the right child (if exists)
            if right_child_index < n:
                comparisons += 1
                array_accesses += 2  # Accessing lst[right_child_index] and lst[largest_index]

                # Highlight the comparison
                persistent_colors[current_root_index] = visualization.COMPARISON_COLOR
                persistent_colors[right_child_index] = visualization.COMPARISON_COLOR
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
                yield comparisons, array_accesses

                if (lst[right_child_index] > lst[largest_index] if ascending else lst[right_child_index] < lst[largest_index]):
                    largest_index = right_child_index

                # Revert to depth color after comparison
                persistent_colors[current_root_index] = visualization.get_color_for_depth(depth)
                persistent_colors[right_child_index] = visualization.get_color_for_depth(depth + 1)

            # If the largest is not the current root, swap and continue heapifying
            if largest_index != current_root_index:
                array_accesses += 4  # 2 reads, 2 writes for the swap
                lst[current_root_index], lst[largest_index] = lst[largest_index], lst[current_root_index]

                # Highlight the swap
                persistent_colors[current_root_index] = visualization.COMPARISON_COLOR
                persistent_colors[largest_index] = visualization.COMPARISON_COLOR
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
                yield comparisons, array_accesses

                # Revert to depth color after the swap
                persistent_colors[current_root_index] = visualization.get_color_for_depth(depth)
                persistent_colors[largest_index] = visualization.get_color_for_depth(calculate_depth(largest_index))

                # Move down to the largest child and continue heapifying
                current_root_index = largest_index
            else:
                break

    n = len(lst)
    last_sorted_index = None

    # Build a max heap (for ascending sort)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(lst, n, i)

    # One by one extract elements from the heap and re-heapify
    for i in range(n - 1, 0, -1):
        array_accesses += 4  # 2 reads, 2 writes for the swap
        lst[i], lst[0] = lst[0], lst[i]  # Swap the root (largest) element with the last element

        # Visualize the swap
        if last_sorted_index is not None:
            persistent_colors[last_sorted_index] = visualization.BAR_COLOR  # Revert the previous sorted element to grey
        persistent_colors[i] = visualization.SORTED_COLOR  # Mark the element in its final position
        persistent_colors[0] = visualization.get_color_for_depth(0)

        last_sorted_index = i

        # Heapify the root element to maintain the max heap property
        yield from heapify(lst, i, 0)

    # Final pass to mark all elements as sorted
    for i in range(n):
        persistent_colors[i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses
        last_sorted_index = i

    return comparisons, array_accesses

def tim_sort(lst, visualization, persistent_colors=None, ascending=True, comparisons=0, array_accesses=0):
    """
    Tim Sort with detailed visualization, combining insertion sort and merge sort.

    Tim Sort is a hybrid sorting algorithm derived from merge sort and insertion sort. 
    It breaks the list into smaller runs, sorts them using insertion sort, and then merges 
    them using merge sort. This approach leverages the natural order in the list for improved efficiency.

    Visualization Details:
    - Insertion sort is used for small segments (runs) and is visualized with comparisons and movements.
    - Merge sort is used to combine these sorted runs.
    - Elements being compared and swapped are highlighted in red.
    - Once an element is placed in its correct position, it is highlighted in green.
    - The final pass turns all elements green one by one to indicate the list is fully sorted.

    Big O Notations:
    - Time Complexity:
        - Best Case: O(n), when the list is already mostly sorted.
        - Average Case: O(n log n), typical case with no particular order in the input data.
        - Worst Case: O(n log n), occurs when the input list is in completely reverse order.
    - Space Complexity: O(n), due to the temporary array used during the merging process.

    Arguments:
    - lst: The list to be sorted.
    - visualization: The visualization object to handle drawing.
    - persistent_colors: A dictionary to track the colors of each element in the visualization.
    - ascending: Whether to sort the list in ascending order (default is True).
    - comparisons: Initial count of comparisons made (for cumulative tracking).
    - array_accesses: Initial count of array accesses made (for cumulative tracking).

    Yields:
    - comparisons: The updated number of comparisons after each significant step.
    - array_accesses: The updated number of array accesses after each significant step.

    Returns:
    - The final counts of comparisons and array accesses after the sorting is complete.
    """


    MIN_RUN = 32

    def insertion_sort(lst, left, right):
        nonlocal comparisons, array_accesses
        last_sorted_index = None

        for i in range(left + 1, right + 1):
            j = i
            current_value = lst[i]

            array_accesses += 2  # Accessing lst[i] (current_value) and lst[j - 1] (while loop)
            comparisons += 1  # Initial comparison in the while loop

            # Highlight the two elements being compared/shifted
            persistent_colors[i - 1] = visualization.COMPARISON_COLOR
            persistent_colors[i] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            # Flag to track if the loop was entered and if an extra comparison/ access should be adjusted
            extra_comparison = False
            extra_access = False

            # Shift elements that are greater/less (based on order) than the current element
            while j > left and ((lst[j - 1] > current_value and ascending) or (lst[j - 1] < current_value and not ascending)):
                
                # Shift the element
                lst[j] = lst[j - 1]
                array_accesses += 2  # Accessing lst[j-1] and assigning to lst[j]

                # Highlight the two elements being compared/shifted
                persistent_colors[j - 1] = visualization.COMPARISON_COLOR
                persistent_colors[j] = visualization.COMPARISON_COLOR
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
                yield comparisons, array_accesses

                if last_sorted_index is not None:
                    persistent_colors[last_sorted_index] = visualization.SORTED_COLOR  # Revert to green if overwritten

                # Revert the previously highlighted elements to grey before moving on
                persistent_colors[j] = visualization.BAR_COLOR
                persistent_colors[j - 1] = visualization.BAR_COLOR

                j -= 1

                extra_comparison = True
                extra_access = True
                comparisons += 1
                array_accesses += 1  # Accessing lst[j - 1] next iteration

            # If the loop was entered, adjust for the extra comparison and access
            if extra_comparison and extra_access:
                comparisons -= 1
                array_accesses -= 1
                
            # Place the current element in its correct position
            lst[j] = current_value
            array_accesses += 1  # Writing current_value back to lst

            if last_sorted_index is not None:
                persistent_colors[last_sorted_index] = visualization.BAR_COLOR  # Revert the previous sorted element to grey

            # Mark the placed element as green to indicate it's in the correct position
            if i == j:
                # Special case: If the current element was already in the correct position, 
                # mark the previous element as sorted (green) and revert the current element to grey
                persistent_colors[j - 1] = visualization.SORTED_COLOR
                persistent_colors[j] = visualization.BAR_COLOR
                last_sorted_index = j - 1
            else:
                # Regular case: Mark the current element as sorted (green)
                persistent_colors[j] = visualization.SORTED_COLOR
                last_sorted_index = j

            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

        persistent_colors[last_sorted_index] = visualization.BAR_COLOR # Reset last sorted element to grey
        persistent_colors[i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

        persistent_colors[i] = visualization.BAR_COLOR # Reset last sorted element to grey

    def merge(lst, left, mid, right):
        nonlocal comparisons, array_accesses
        temp = []

        i = left
        j = mid + 1

        while i <= mid and j <= right:
            comparisons += 1  # Comparing elements
            array_accesses += 2  # Accessing elements at i and j

            # Highlight the left and right boundaries during the merge process.
            persistent_colors[left] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[right] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[mid] = visualization.PRIMARY_ACTIVE_COLOR 

            if (lst[i] <= lst[j] and ascending) or (lst[i] >= lst[j] and not ascending):
                temp.append(lst[i])
                array_accesses += 1  # Accessing lst[i] to append it to temp

                # Highlight the element being merged in red.
                persistent_colors[i] = visualization.COMPARISON_COLOR
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
                yield comparisons, array_accesses

                # Revert the element color after it is processed.
                persistent_colors[i] = visualization.BAR_COLOR
                
                i += 1
            else:
                temp.append(lst[j])
                array_accesses += 1  # Accessing lst[j] to append it to temp

                # Highlight the element being merged in red.
                persistent_colors[j] = visualization.COMPARISON_COLOR
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
                yield comparisons, array_accesses

                # Revert the element color after it is processed.
                persistent_colors[j] = visualization.BAR_COLOR

                j += 1

        # Add any remaining elements from the left subarray to the temp array.
        while i <= mid:
            array_accesses += 1  # Accessing lst[i] to append it to temp
            temp.append(lst[i])

            # Ensure left and right boundaries are highlighted during the merge
            persistent_colors[left] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[right] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[mid] = visualization.PRIMARY_ACTIVE_COLOR 

            # Highlight the element being merged in red.
            persistent_colors[i] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            # Revert the element color after it is processed.
            persistent_colors[i] = visualization.BAR_COLOR

            i += 1

        # Add any remaining elements from the right subarray
        while j <= right:
            temp.append(lst[j])
            array_accesses += 1  # Accessing lst[j] to append it to temp

            # Ensure left and right boundaries are highlighted during the merge
            persistent_colors[left] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[right] = visualization.SECONDARY_ACTIVE_COLOR
            persistent_colors[mid] = visualization.PRIMARY_ACTIVE_COLOR 

            # Highlight the element being merged in red.
            persistent_colors[j] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            # Revert the element color after it is processed.
            persistent_colors[j] = visualization.BAR_COLOR

            j += 1

        # Copy the sorted elements from the temp array back to the original array
        for k in range(len(temp)):
            lst[left + k] = temp[k]
            array_accesses += 2  # Accessing lst[left + k] and temp[k]

            # Ensure left and right boundaries are highlighted during the merge
            persistent_colors[left] = visualization.BAR_COLOR
            persistent_colors[right] = visualization.BAR_COLOR
            persistent_colors[mid] = visualization.BAR_COLOR 
            persistent_colors[left + k] = visualization.SORTED_COLOR

            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            # Revert the color after visualization.
            persistent_colors[left + k] = visualization.BAR_COLOR

    n = len(lst)

    # Sort small runs using insertion sort
    for start in range(0, n, MIN_RUN):
        end = min(start + MIN_RUN - 1, n - 1)
        yield from insertion_sort(lst, start, end)

    # Merge sorted runs
    size = MIN_RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))

            if mid < right:
                yield from merge(lst, left, mid, right)

        size *= 2

    # Final pass to mark all elements as sorted
    for i in range(n):
        persistent_colors[i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

    return comparisons, array_accesses

def tree_sort(lst, visualization, persistent_colors=None, ascending=True, comparisons=0, array_accesses=0):
    """
    Performs Tree Sort with detailed visualization.

    Tree Sort is a comparison-based sorting algorithm that builds a binary search tree (BST)
    from the elements of the list, then performs an in-order traversal to produce the sorted list.
    This implementation includes visualization steps to highlight every comparison and array access,
    and uses color coding to indicate the depth of elements in the BST.

    Visualization Details:
    - Every access and comparison is highlighted in red and then reverted to its depth color.
    - Depth levels are indicated by varying colors.
    - Once an element is placed in its correct position, it is highlighted in green.
    - The final pass turns all elements green one by one to indicate the list is fully sorted.

    Big O Notations:
    - Time Complexity:
      - Best Case: O(n log n) when the tree is balanced.
      - Average Case: O(n log n), typical case for randomly ordered inputs.
      - Worst Case: O(n^2) when the tree becomes a degenerate (linked list).
    - Space Complexity: O(n) for storing the tree.

    Arguments:
    - lst: The list of elements to be sorted.
    - visualization: The visualization object responsible for rendering the sorting process.
    - persistent_colors: A dictionary tracking the colors of each element in the visualization.
    - ascending: Boolean indicating whether to sort in ascending (True) or descending (False) order.
    - comparisons: Running total of comparisons made so far.
    - array_accesses: Running total of array accesses made so far.

    Yields:
    - comparisons: The updated number of comparisons after each significant step.
    - array_accesses: The updated number of array accesses after each significant step.

    Returns:
    - The final counts of comparisons and array accesses after the sorting is complete.
    """

    class TreeNode:
        def __init__(self, index, depth=0):
            self.left = None
            self.right = None
            self.index = index
            self.depth = depth

    def insert(root, index, depth):
        """Inserts a new node with the given index in the BST, with array access and comparison counting."""
        nonlocal comparisons, array_accesses
                
        if root is None:
            return TreeNode(index, depth)
        else:
            comparisons += 1
            array_accesses += 2
            
            # Highlight the comparison using the index and depth color
            persistent_colors[root.index] = visualization.PRIMARY_ACTIVE_COLOR
            persistent_colors[index] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses
            
            # Revert to depth color after comparison
            persistent_colors[root.index] = visualization.get_color_for_depth(root.depth)
            persistent_colors[index] = visualization.get_color_for_depth(depth)

            if (lst[root.index] < lst[index] and ascending) or (lst[root.index] > lst[index] and not ascending):
                if root.right is None:
                    root.right = TreeNode(index, depth + 1)
                    persistent_colors[index] = visualization.get_color_for_depth(depth + 1)
                else:
                    root.right = yield from insert(root.right, index, depth + 1)
            else:
                if root.left is None:
                    root.left = TreeNode(index, depth + 1)
                    persistent_colors[index] = visualization.get_color_for_depth(depth + 1)
                else:
                    root.left = yield from insert(root.left, index, depth + 1)
        return root

    def in_order_traversal(root, sorted_indices, visualization, persistent_colors, comparisons=0, array_accesses=0):
        """Performs an in-order traversal of the BST and appends the indices to the sorted_indices list."""
        if root:
            # Traverse the left subtree
            comparisons, array_accesses = yield from in_order_traversal(root.left, sorted_indices, visualization, persistent_colors, comparisons, array_accesses)

            # Access the root node
            array_accesses += 1
            sorted_indices.append(root.index)

            # Highlight the access in red using the index
            persistent_colors[root.index] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            # Revert to grey 
            persistent_colors[root.index] = visualization.BAR_COLOR

            # Traverse the right subtree
            comparisons, array_accesses = yield from in_order_traversal(root.right, sorted_indices, visualization, persistent_colors, comparisons, array_accesses)

        return comparisons, array_accesses

    if not lst:
        return comparisons, array_accesses

    # Initialize the BST root
    root = None
    n = len(lst)

    # Insert elements into the BST
    for i in range(n):
        root = yield from insert(root, i, depth=0)

    draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
    yield comparisons, array_accesses

    # In-order traversal to get the sorted indices
    sorted_indices = []
    comparisons, array_accesses = yield from in_order_traversal(root, sorted_indices, visualization, persistent_colors, comparisons, array_accesses)

    # Copy the sorted elements back to the original list in order
    sorted_lst = []
    for i in sorted_indices:
        array_accesses += 1  # Accessing lst[i]
        sorted_lst.append(lst[i])

    for i in range(n):
        array_accesses += 2
        lst[i] = sorted_lst[i]

        # Highlight as sorted (green)
        persistent_colors[i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

        # Revert the color after visualization.
        persistent_colors[i] = visualization.BAR_COLOR

    # Final pass to mark all elements as sorted
    for i in range(n):
        persistent_colors[i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

    return comparisons, array_accesses

def shell_sort(lst, visualization, persistent_colors=None, ascending=True):
    """
    Performs Shell Sort with detailed visualization.

    Shell Sort is an in-place comparison-based sorting algorithm that generalizes insertion sort to allow the exchange 
    of items that are far apart. The method starts by sorting elements far apart from each other and progressively 
    reduces the gap between them. This approach is more efficient than a simple insertion sort, especially for larger 
    arrays.

    Visualization Details:
    - Elements being compared are highlighted in red.
    - Elements that are shifted are highlighted in red.
    - Once an element is in its correct position relative to the current gap, it is highlighted in green.
    - The final pass turns all elements green one by one to indicate the list is fully sorted.

    Big O Notations:
    - Time Complexity:
      - Best Case: O(n log n), occurs when the array is already partially sorted and minimal shifts are needed.
      - Average Case: Depends on the gap sequence used; typically around O(n^(3/2)) for the default gap sequence.
      - Worst Case: O(n^2), occurs when the array is in reverse order and the gaps are not optimized.
      - Note: The performance can be optimized by using more efficient gap sequences, such as the Sedgewick sequence.

    - Space Complexity: O(1), as the algorithm is in-place and does not require additional storage.

    Arguments:
    - lst: The list of elements to be sorted.
    - visualization: The visualization object responsible for rendering the sorting process.
    - persistent_colors: A dictionary tracking the colors of each element in the visualization.
    - ascending: Boolean indicating whether to sort in ascending (True) or descending (False) order.

    Yields:
    - comparisons: The updated number of comparisons after each significant step.
    - array_accesses: The updated number of array accesses after each significant step.

    Returns:
    - The final counts of comparisons and array accesses after the sorting is complete.
    """

    comparisons = 0
    array_accesses = 0

    n = len(lst)
    last_sorted_index = None
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = lst[i]
            j = i

            array_accesses += 2  # Accessing lst[i] and lst[j - gap]
            comparisons += 1  # Initial comparison in the while loop

            # Visualization for the two elements being compared before shifting
            persistent_colors[i] = visualization.COMPARISON_COLOR
            persistent_colors[j - gap] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

            # Gap insertion sort
            while j >= gap and ((lst[j - gap] > temp and ascending) or (lst[j - gap] < temp and not ascending)):
                
                comparisons += 1  # Comparison for the next iteration
                array_accesses += 1  # Accessing lst[j - gap] next iteration

                # Shift the previous element by the gap distance to make room for the current element
                lst[j] = lst[j - gap]
                array_accesses += 2  # Accessing lst[j-1] and assigning to lst[j]

                # Highlight the two elements being shifted in red
                persistent_colors[j - gap] = visualization.COMPARISON_COLOR
                persistent_colors[j] = visualization.COMPARISON_COLOR

                # Highlight the element that was shifted
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
                yield comparisons, array_accesses

                # Revert the previously highlighted elements to grey before moving on
                persistent_colors[j] = visualization.BAR_COLOR
                persistent_colors[j - gap] = visualization.BAR_COLOR

                if last_sorted_index is not None:
                    persistent_colors[last_sorted_index] = visualization.SORTED_COLOR  # Revert to green if overwritten

                j -= gap


            # Place the current element in its correct position
            lst[j] = temp
            array_accesses += 1  # Assigning temp to lst[j]

            if last_sorted_index is not None:
                persistent_colors[last_sorted_index] = visualization.BAR_COLOR  # Revert the previous sorted element to grey
        
            # Mark the placed element as green to indicate it's in the correct position
            if i == j:
                # Special case: If the current element was already in the correct position, 
                # mark the previous element as sorted (green) and revert the current element to grey
                persistent_colors[j - gap] = visualization.SORTED_COLOR
                persistent_colors[j] = visualization.BAR_COLOR
                last_sorted_index = j - gap
            else:
                # Regular case: Mark the current element as sorted (green)
                persistent_colors[j] = visualization.SORTED_COLOR
                last_sorted_index = j

            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
            yield comparisons, array_accesses

        gap //= 2

    persistent_colors[last_sorted_index] = visualization.BAR_COLOR # Reset last sorted element to grey
    persistent_colors[i] = visualization.SORTED_COLOR
    draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
    yield comparisons, array_accesses

    persistent_colors[i] = visualization.BAR_COLOR # Reset last sorted element to grey

    # Final pass to mark all elements as sorted
    for i in range(n):
        persistent_colors[i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

    return comparisons, array_accesses

def cocktail_shaker_sort(lst, visualization, persistent_colors, ascending=True):
    """
    Cocktail Shaker Sort with detailed visualization.
    This algorithm is a variation of Bubble Sort that sorts in both directions on each pass through the list.
    It alternates between moving larger elements to the end and smaller elements to the start, making it more efficient than standard Bubble Sort in some cases.

    Visualization Details:
    - Elements being compared are highlighted in red.
    - After a swap (if needed), the swapped elements remain highlighted in red.
    - Once an element reaches its correct position, it is highlighted in green.
    - The final pass turns all elements green one by one to indicate the list is fully sorted.

    Big O Notations:
    - Time Complexity: 
      - Best Case: O(n) when the list is already sorted (due to the early exit optimization).
      - Average Case: O(n^2) due to two nested loops.
      - Worst Case: O(n^2) when the list is sorted in reverse order.
    - Space Complexity: O(1), as it only requires a constant amount of additional space.

    Arguments:
    lst -- the list to be sorted.
    visualization -- the visualization object to handle drawing.
    persistent_colors -- a dictionary to track the colors of each element in the visualization.
    ascending -- whether to sort the list in ascending order (default is True).

    Returns:
    Yields comparisons, array_accesses, and swaps for each step of the visualization.
    """
    
    comparisons = 0
    array_accesses = 0
    swaps = 0

    n = len(lst)
    start = 0
    end = n - 1
    last_sorted_index = None

    while start < end:
        swapped = False

        # Forward pass (left to right)
        for i in range(start, end):
            comparisons += 1  # Count the comparison
            array_accesses += 2  # Accessing lst[i] and lst[i + 1] counts as 2 accesses

            # Highlight the two elements being compared
            persistent_colors[i] = visualization.COMPARISON_COLOR
            persistent_colors[i + 1] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
            yield comparisons, array_accesses, swaps

            if (lst[i] > lst[i + 1] and ascending) or (lst[i] < lst[i + 1] and not ascending):
                # Swap if the elements are out of order
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
                array_accesses += 4  # Swapping involves 4 accesses (2 reads, 2 writes)
                swaps += 1  # Count the swap
                swapped = True

                # Highlight the swapped elements
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
                yield comparisons, array_accesses, swaps

            # Revert the compared elements back to their default color
            persistent_colors[i] = visualization.BAR_COLOR
            persistent_colors[i + 1] = visualization.BAR_COLOR

        if last_sorted_index is not None:
            persistent_colors[last_sorted_index] = visualization.BAR_COLOR  # Revert the previous sorted element to grey

        # Mark the last element of the current forward pass as sorted
        persistent_colors[end] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
        yield comparisons, array_accesses, swaps

        last_sorted_index = end

        end -= 1  # Reduce the range for the next pass

        if not swapped:
            break  # If no swaps occurred, the list is sorted

        # Backward pass (right to left)
        swapped = False
        for i in range(end, start, -1):
            comparisons += 1  # Count the comparison
            array_accesses += 2  # Accessing lst[i] and lst[i - 1] counts as 2 accesses

            # Highlight the two elements being compared
            persistent_colors[i] = visualization.COMPARISON_COLOR
            persistent_colors[i - 1] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
            yield comparisons, array_accesses, swaps

            if (lst[i] < lst[i - 1] and ascending) or (lst[i] > lst[i - 1] and not ascending):
                # Swap if the elements are out of order
                lst[i], lst[i - 1] = lst[i - 1], lst[i]
                array_accesses += 4  # Swapping involves 4 accesses (2 reads, 2 writes)
                swaps += 1  # Count the swap
                swapped = True

                # Highlight the swapped elements
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
                yield comparisons, array_accesses, swaps

            # Revert the compared elements back to their default color
            persistent_colors[i] = visualization.BAR_COLOR
            persistent_colors[i - 1] = visualization.BAR_COLOR

        if last_sorted_index is not None:
            persistent_colors[last_sorted_index] = visualization.BAR_COLOR  # Revert the previous sorted element to grey

        # Mark the first element of the current backward pass as sorted
        persistent_colors[start] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
        yield comparisons, array_accesses, swaps

        last_sorted_index = start

        start += 1  # Increase the range for the next pass

        if not swapped:
            break  # If no swaps occurred, the list is sorted
    
    persistent_colors[last_sorted_index] = visualization.BAR_COLOR

    # Final pass to mark all elements as fully sorted by turning them green
    for i in range(n):
        persistent_colors[i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
        yield comparisons, array_accesses, swaps

def comb_sort(lst, visualization, persistent_colors, ascending=True):
    """
    Comb Sort with detailed visualization.
    This algorithm is an improvement over Bubble Sort by eliminating small values near the end of the list
    early in the sorting process, which Bubble Sort takes a long time to address. The main feature of Comb Sort
    is the use of a shrinking gap between compared elements.

    Visualization Details:
    - Elements being compared are highlighted in red.
    - After a swap (if needed), the swapped elements remain highlighted in red.
    - Once an element reaches its correct position, it is highlighted in green.
    - The final pass turns all elements green one by one to indicate the list is fully sorted.

    Big O Notations:
    - Time Complexity: 
      - Best Case: O(n log n) when the list is already nearly sorted.
      - Average Case: O(n^2/log n) due to the shrinking gap.
      - Worst Case: O(n^2) when the list is sorted in reverse order.
    - Space Complexity: O(1), as it only requires a constant amount of additional space.

    Arguments:
    lst -- the list to be sorted.
    visualization -- the visualization object to handle drawing.
    persistent_colors -- a dictionary to track the colors of each element in the visualization.
    ascending -- whether to sort the list in ascending order (default is True).

    Returns:
    Yields comparisons, array_accesses, and swaps for each step of the visualization.
    """
    
    comparisons = 0
    array_accesses = 0
    swaps = 0

    n = len(lst)
    gap = n
    shrink_factor = 1.3
    sorted = False

    while not sorted:
        # Update the gap for the next comb
        gap = int(gap / shrink_factor)
        if gap <= 1:
            gap = 1
            sorted = True  # Assume the list is sorted, we will check below

        index = 0
        while index + gap < n:
            comparisons += 1  # Each comparison is counted
            array_accesses += 2  # Accessing lst[index] and lst[index + gap] counts as 2 accesses

            # Highlight the two elements being compared
            persistent_colors[index] = visualization.COMPARISON_COLOR
            persistent_colors[index + gap] = visualization.COMPARISON_COLOR
            draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
            yield comparisons, array_accesses, swaps

            if (lst[index] > lst[index + gap] and ascending) or (lst[index] < lst[index + gap] and not ascending):
                # Swap the elements if they are out of order
                lst[index], lst[index + gap] = lst[index + gap], lst[index]
                array_accesses += 4  # Swapping involves 4 accesses (2 reads, 2 writes)
                swaps += 1  # Count the swap
                sorted = False  # If a swap is made, the list is not fully sorted

                # Highlight the swapped elements
                draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
                yield comparisons, array_accesses, swaps

            # Revert the compared elements back to their default color
            persistent_colors[index] = visualization.BAR_COLOR
            persistent_colors[index + gap] = visualization.BAR_COLOR

            index += 1

    # Final pass to mark all elements as fully sorted by turning them green
    for i in range(n):
        persistent_colors[i] = visualization.SORTED_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses, swaps=swaps)
        yield comparisons, array_accesses, swaps

def bogo_sort(lst, visualization, persistent_colors, ascending=True):
    """
    Bogo Sort with detailed visualization.
    Bogo Sort is an extremely inefficient sorting algorithm that generates random permutations of the list
    until it finds one that is sorted. It's primarily used for educational purposes to illustrate inefficiency.

    Visualization Details:
    - The current permutation being checked is highlighted in red.
    - Once a sorted permutation is found, all elements are highlighted in green.
    - The sorting process is visualized step-by-step, showing each random shuffle.

    Big O Notations:
    - Time Complexity: 
      - Best Case: O(n) when the list is sorted on the first permutation.
      - Average Case: O((n+1)!) due to the factorial number of possible permutations.
      - Worst Case: Unbounded, theoretically could run indefinitely.
    - Space Complexity: O(1), as it only requires a constant amount of additional space.

    Arguments:
    lst -- the list to be sorted.
    visualization -- the visualization object to handle drawing.
    persistent_colors -- a dictionary to track the colors of each element in the visualization.
    ascending -- whether to sort the list in ascending order (default is True).

    Returns:
    Yields comparisons and array_accesses for each step of the visualization.
    """

    comparisons = 0
    array_accesses = 0

    def is_sorted(lst):
        """Check if the list is sorted and count array accesses."""
        nonlocal comparisons, array_accesses
        for i in range(len(lst) - 1):
            array_accesses += 2  # Accessing lst[i] and lst[i + 1] counts as 2 accesses
            comparisons += 1  # Each comparison is counted
            if ascending:
                if lst[i] > lst[i + 1]:
                    return False
            else:
                if lst[i] < lst[i + 1]:
                    return False
        return True

    while not is_sorted(lst):
        # Highlight the entire list as the current permutation being checked
        for i in range(len(lst)):
            persistent_colors[i] = visualization.COMPARISON_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

        # Randomly shuffle the list
        random.shuffle(lst)
        array_accesses += len(lst)  # Shuffling involves accessing each element once

        # Revert the colors after checking the permutation
        for i in range(len(lst)):
            persistent_colors[i] = visualization.BAR_COLOR
        draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
        yield comparisons, array_accesses

    # Final pass to mark all elements as fully sorted by turning them green
    for i in range(len(lst)):
        persistent_colors[i] = visualization.SORTED_COLOR
    draw_list(visualization, persistent_colors=persistent_colors, comparisons=comparisons, array_accesses=array_accesses)
    yield comparisons, array_accesses


