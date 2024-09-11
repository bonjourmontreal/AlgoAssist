from .sorting_algorithms import *
from .helpers import *
from .draw_utils import *
from ui import *
from .constants import *
from .visualizer import initialize_sorting_visualizer

def launch_visualizer():
    # Initialize visualization settings and state
    visualizer = initialize_sorting_visualizer(
        size=LIST_MIN_SIZE, 
        speed=MIN_SPEED, 
        sorting_algorithm=bubble_sort, 
        sorting_algo_name="Bubble Sort"
    )

    return visualizer.run(visualizer)

if __name__ == "__main__":
    launch_visualizer()