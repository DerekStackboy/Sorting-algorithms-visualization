
import time
from mtable import MonitoredTable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 50  # number of elements, can be changed
FPS = 60  # fps for parameter interval 



table = MonitoredTable(0, 1000, N, "R") # also can write mode "S", "T" or "A"

###############################################
def stooge_sort(arr, l, h):
    if l >= h:
        return
   
    # If first element is smaller
    # than last,swap them
    if arr[l]>arr[h]:
        t = arr[l]
        arr[l] = arr[h]
        arr[h] = t
   
    # If there are more than 2 elements in
    # the array
    if h-l+1 > 2:
        t = (int)((h-l+1)/3)
   
        # Recursively sort first 2/3 elements
        stooge_sort(arr, l, (h-t))
   
        # Recursively sort last 2/3 elements
        stooge_sort(arr, l+t, (h))
   
        # Recursively sort first 2/3 elements
        # again to confirm
        stooge_sort(arr, l, (h-t))
# counting sorting time for this algorithm
###############################################
algorithm = "Stooge sort"
t0 = time.perf_counter()
stooge_sort(table, 0, len(table) - 1)
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

    # animation is accumulated here, with the show command
    ani = FuncAnimation(fig, update, frames=range(len(table.full_copy)), blit=True, interval=1000./FPS, repeat=False)
    plt.show()

