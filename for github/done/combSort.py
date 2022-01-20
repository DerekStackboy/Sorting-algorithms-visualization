
import time
from mtable import MonitoredTable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 50  # number of elements, can be changed
FPS = 60  # fps for parameter interval 

table = MonitoredTable(0, 1000, N, "R") # also can write mode "S", "T" or "A"

###############################################
# To find next gap from current
def getNextGap(gap):
    # Shrink gap by Shrink factor
    gap = (gap * 10)//13
    if gap < 1:
        return 1
    return gap
 
# Function to sort arr[] using Comb Sort
def comb_sort(arr):
    n = len(arr)
    # Initialize gap
    gap = n
    # Initialize swapped as true to make sure that
    # loop runs
    swapped = True
    # Keep running while gap is more than 1 and last
    # iteration caused a swap
    while gap !=1 or swapped == 1:
        # Find next gap
        gap = getNextGap(gap)
 
        # Initialize swapped as false so that we can
        # check if swap happened or not
        swapped = False
        # Compare all elements with current gap
        for i in range(0, n-gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap]=arr[i + gap], arr[i]
                swapped = True

# counting sorting time for this algorithm
###############################################
algorithm = "Comb sort"
t0 = time.perf_counter()
comb_sort(table)
delta_t = time.perf_counter() - t0
###############################################
def update(frame):
    txt.set_text(f"Operations count = {frame}")
    for rectangle, height in zip(container.patches, table.full_copy[frame]):
        rectangle.set_height(height)
        rectangle.set_color("darkblue")

    idx, op = table.activity(frame)
    if op == "get":
        container.patches[idx].set_color("green")
    elif op == "set":
        container.patches[idx].set_color("red")

    return (txt, *container)
###############################################


if __name__ == "__main__":

    print(f"Sorting: {algorithm}")
    print(f"table sorted in time {delta_t*1000:.1f} ms. Operations count: {len(table.full_copy):.0f}.")
    ###############################################

    # configuration to display the histogram
    plt.rcParams["font.size"] = 16
    fig, ax = plt.subplots(figsize=(16, 8))
    container = ax.bar(np.arange(0, len(table), 1), table.full_copy[0], align="edge", width=0.8)
    fig.suptitle(f"Sorting algorithm: {algorithm}")
    ax.set(xlabel="Index", ylabel="Value")
    ax.set_xlim([0, N])
    txt = ax.text(0.01, 0.99, "", ha="left", va="top", transform=ax.transAxes)

    # function that updates the state of individual frames to be displayed


    # animation is accumulated here, with the show command
    ani = FuncAnimation(fig, update, frames=range(len(table.full_copy)), blit=True, interval=1000./FPS, repeat=False)
    plt.show()

