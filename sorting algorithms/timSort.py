
import time
from mtable import MonitoredTable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 50  # number of elements, can be changed
FPS = 60  # fps for parameter interval 



table = MonitoredTable(0, 1000, N, "R") # also can write mode "S", "T" or "A"

MIN_MERGE = 32
###############################################
def calcMinRun(n):
	""" Returns the minimum length of a
	run from 23 - 64 so that
	the len(array)/minrun is less than or
	equal to a power of 2.

	e.g. 1=>1, ..., 63=>63, 64=>32, 65=>33,
	..., 127=>64, 128=>32, ...
	"""
	r = 0
	while n >= MIN_MERGE:
		r |= n & 1
		n >>= 1
	return n + r


#sorts array from left index to right index which is of size atmost RUN
def insertionSort(arr, left, right):
	for i in range(left + 1, right + 1):
		j = i
		while j > left and arr[j] < arr[j - 1]:
			arr[j], arr[j - 1] = arr[j - 1], arr[j]
			j -= 1


def merge(arr, l, m, r):
	
	# original array is broken in two parts
	# left and right array
	len1, len2 = m - l + 1, r - m
	left, right = [], []
	for i in range(0, len1):
		left.append(arr[l + i])
	for i in range(0, len2):
		right.append(arr[m + 1 + i])

	i, j, k = 0, 0, l
	
	# after comparing, we merge those two array in larger sub array
	while i < len1 and j < len2:
		if left[i] <= right[j]:
			arr[k] = left[i]
			i += 1

		else:
			arr[k] = right[j]
			j += 1

		k += 1

	while i < len1:
		arr[k] = left[i]
		k += 1
		i += 1
	while j < len2:
		arr[k] = right[j]
		k += 1
		j += 1


def tim_sort(arr):

	n = len(arr)
	minRun = calcMinRun(n)
	
	# Sort individual subarrays of size RUN
	for start in range(0, n, minRun):
		end = min(start + minRun - 1, n - 1)
		insertionSort(arr, start, end)

	# Start merging from size RUN (or 32). 
	size = minRun
	while size < n:
		
		for left in range(0, n, 2 * size):
			mid = min(n - 1, left + size - 1)
			right = min((left + 2 * size - 1), (n - 1))

			if mid < right:
				merge(arr, left, mid, right)

		size = 2 * size
# counting sorting time for this algorithm
###############################################
algorithm = "Tim sort"
t0 = time.perf_counter()
tim_sort(table)
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

