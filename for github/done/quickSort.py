
import time
from mtable import MonitoredTable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 50  # number of elements, can be changed
FPS = 60  # fps for parameter interval 



table = MonitoredTable(0, 1000, N, "R") # also can write mode "S", "T" or "A"

###############################################
def swap(a, b, arr):
     if a != b:
            temp = arr[a]
            arr[a] = arr[b]
            arr[b] = temp

def partition(elements, start, end):
    pivot_index = start
    pivot = elements[pivot_index]


    while start < end:
        while start < len(elements) and elements[start] <= pivot:
            start += 1
        while elements[end] > pivot:
            end -= 1

        if start < end:
            swap(start, end, elements)

    swap(pivot_index, end, elements)
    
    return end

def quick_sort(elements, start, end):
    if start < end:
        partition_index =  partition(elements, start, end)

        quick_sort(elements, start, partition_index - 1) #left partition
        quick_sort(elements, partition_index + 1, end) #right partition 
    
    return elements




# counting sorting time for this algorithm
###############################################
algorithm = "Quick sort"
t0 = time.perf_counter()
table = quick_sort(table, 0, len(table) - 1)
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

