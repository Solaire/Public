import pygame
import random
import sys

# Font
pygame.font.init()
FONT_1 = pygame.font.SysFont("comicsans", 30) 
FONT_2 = pygame.font.SysFont("comicsans", 20)

# Colours
BLACK   = (0, 0, 0)       
WHITE   = (255, 255, 255)   # Unsorted array elements
RED     = (255, 0, 0)       # Comparing two elements
GREEN   = (97, 222, 42)    # Selected element (eg. pivot)
ORANGE  = (255, 128, 0)     # Sorted elements

# Text
TEXT_ENTER      = FONT_1.render("PRESS 'ENTER' TO PERFORM SORTING.", 1, WHITE)
TEXT_NEW_ARR    = FONT_1.render("PRESS 'R' FOR A NEW ARRAY.", 1, WHITE)
TEXT_ARROWS     = FONT_1.render("PRESS 'LEFT' or 'RIGHT' to select sorting algorithm", 1, WHITE)

# Window size 
WIDTH   = 900
HEIGHT  = 650

# Timer
DELAY_MS = 5

# Title and icon
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting algorithms")

# Arrays
ARRAY_SIZE      = 300

# Algorithms
MERGE_SORT      = 0
QUICK_SORT      = 1
BUBBLE_SORT     = 2
SELECTION_SORT  = 3
INSERTION_SORT  = 4

array_main      = [0] * ARRAY_SIZE
array_colour    = [WHITE] * ARRAY_SIZE
algorithms      = ["mergesort", "quicksort", "bubblesort", "selection sort", "insertion sort"]
current_algorithm = MERGE_SORT

'''
Generate a new array of random values
'''
def GenerateRandomArray(): 
    array_min = ARRAY_SIZE
    array_max = 0
    global_min = 10
    global_max = HEIGHT - 200

    for i in range(0, len(array_main)): 
        array_colour[i]  = WHITE
        array_main[i]    = random.randrange(1, ARRAY_SIZE)
        if array_min > array_main[i]:
            array_min = array_main[i]
        elif array_max < array_main[i]:
            array_max = array_main[i]

    # Normalise the array to fit within range, otherwise the value differences will look tiny
    for i in range(0, len(array_main)):
        stretched = (array_main[i] - array_min) * (global_max / (array_max - array_min)) + global_min
        array_main[i] = int(stretched)

'''
Redraw the screen.
Progress the timer by the delay 
Check for exit input so we can quit mid-sorting
'''
def Redraw(): 
    SCREEN.fill(BLACK) 

    Draw() 
    pygame.display.update() 
    pygame.time.delay(DELAY_MS)

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            sys.exit(0)

'''
Draw to screen
'''
def Draw():
    txt_current_algorithm  = FONT_2.render("ALGORITHM USED: " + algorithms[current_algorithm], 1, WHITE)

    SCREEN.blit(TEXT_ENTER, (20, 20))
    SCREEN.blit(TEXT_NEW_ARR, (20, 40))
    SCREEN.blit(TEXT_ARROWS, (20, 60))
    SCREEN.blit(txt_current_algorithm, (600, 60))

    line_width      = (WIDTH - ARRAY_SIZE) // ARRAY_SIZE # Width of the line itself when drawn
    element_width   = WIDTH / ARRAY_SIZE                 # Width of the element with potential gap (draw x position)

    pygame.draw.line(SCREEN, WHITE, (0, 95), (900, 95), 6)

    # Draw the array elements as a bar-chart sort of thing
    for i in range(0, ARRAY_SIZE):
        pygame.draw.line(SCREEN, array_colour[i], (element_width * i, HEIGHT), (element_width * i, HEIGHT - array_main[i]), line_width)

'''
Merge sort for the sort visualiser
Divide the array into smaller sub-lists (until each sub-array contains one element)
Recursively merge the sub-lists into sorted sublists until one list remains
'''
def VisualMergesort(array, left, right):
    mid1    = (left + right) // 2   # End of the left sub-array
    mid2    = mid1 + 1              # End of the right sub-array

    if left < right: # Split until the left index is the same as right index (single element array)
        VisualMergesort(array, left, mid1)
        VisualMergesort(array, mid2, right)
        VisualMerge(array, left, mid1, mid2, right)

'''
Merge the subarrays
Part of the visual merge sort algorithm
'''
def VisualMerge(array, lx, ly, rx, ry):
    iL      = lx
    iR      = rx
    temp    = []

    pygame.event.pump()

    # Merge the sub-arrays
    while iL <= ly and iR <= ry:
        array_colour[iL] = RED # Show on the visualiser that we are comparing two elements
        array_colour[iR] = RED # Show on the visualiser that we are comparing two elements
        Redraw() 
        array_colour[iL] = WHITE # Back to normal colour
        array_colour[iR] = WHITE # Back to normal colour

        if array[iL] < array[iR]:
            temp.append(array[iL])
            iL += 1
        else:
            temp.append(array[iR])
            iR += 1

    # Add left over elements from the left or right array
    # The loop above will ensure that only one of the sub-arrays will be left over
    while iL <= ly:
        array_colour[iL] = RED # Show on the visualiser that we are comparing two elements
        Redraw() 
        array_colour[iL] = WHITE # Back to normal colour
        temp.append(array[iL])
        iL += 1
    while iR <= ry:
        array_colour[iR] = RED # Show on the visualiser that we are comparing two elements
        Redraw() 
        array_colour[iR] = WHITE # Back to normal colour
        temp.append(array[iR])
        iR += 1
    
    # Purely for the visualiser.
    # At the end of the sorting, reiterate the now-sorted array to draw the sorted array
    iT = 0
    for iA in range(lx, ry + 1):
        pygame.event.pump()
        array[iA] = temp[iT]
        iT += 1
        array_colour[iA] = GREEN 
        Redraw() 
        if ry - lx == len(array) - 1:
            array_colour[iA] = ORANGE 
        else:  
            array_colour[iA] = WHITE 

'''
Merge sort (proper implementation)
Divide the array into smaller sub-lists (until each sub-array contains one element)
Recursively merge the sub-lists into sorted sublists until one list remains
'''
def MergeSort(array):
    if len(array) > 1:
        mid = len(array) // 2
        Left = array[:mid]
        Right = array[mid:]

        # Separate into smaller and smaller sub-arrays.
        MergeSort(Left)
        MergeSort(Right)

        iL = 0 # Index of the left sub-array
        iR = 0 # Index of the right sub-array
        iA = 0 # Index of the merged sub-array

        # Merge the sub-arrays
        while iL < len(Left) and iR < len(Right):
            if Left[iL] < Right[iR]:
                array[iA] = Left[iL]
                iL += 1
            else:
                array[iA] = Right[iR]
                iR += 1
            iA += 1
        
        # Add left over elements from the left or right array
        # The loop above will ensure that only one of the sub-arrays will be left over
        while iL < len(Left):
            array[iA] = Left[iL]
            iL += 1
            iA += 1
        while iR < len(Right):
            array[iA] = Right[iR]
            iR += 1
            iA += 1

'''
Quicksort for the sort visualiser
Pick a pivot in the middle of the current partition
'''
def VisualQuicksort(array, left, right):
    if left < right:
        iP = VisualPartition(array, left, right)
        VisualQuicksort(array, left, iP)
        VisualQuicksort(array, iP + 1, right)

'''
Compare the values left of the pivot the the items right of the pivot, swapping them if needed
Recursively partition and compare teh array until sorted
'''
def VisualPartition(array, left, right):
    iP    = (left + right) // 2 # pivot index
    pivot = array[iP]

    # Set initial colours for left, right and pivot
    array_colour[iP]    = GREEN # Pivot
    array_colour[left]  = RED
    array_colour[right] = RED
    Redraw() 

    iL = left   - 1
    iR = right  + 1

    while True:
        pygame.event.pump() 

        array_colour[iP]    = GREEN # Pivot

        iL += 1
        if iL - 1 >= left: # Since iL might start at -1, check so that we're in range
            array_colour[iL - 1]     = WHITE
        array_colour[iL]     = RED 
        Redraw()
        while array[iL] < pivot:
            array_colour[iL]     = WHITE
            array_colour[iL + 1] = RED 
            Redraw()

            iL += 1

        iR -= 1
        if iR + 1 <= right: # Since iR might start at len_array + 1, check so that we're in range
            array_colour[iR + 1]     = WHITE
        array_colour[iR]     = RED
        Redraw()
        while array[iR] > pivot:
            array_colour[iR]     = WHITE
            array_colour[iR - 1] = RED 
            Redraw()

            iR -= 1

        if iL >= iR:
            array_colour[iL] = WHITE
            array_colour[iR] = WHITE
            array_colour[iP] = WHITE
            Redraw() 

            return iR

        array[iL], array[iR] = array[iR], array[iL]
        
        # We are swapping the values of iL and iR
        # Make sure the pivot is moved to the swapped index
        if iL == iP:
            iP = iR
        elif iR == iP:
            iP = iL

'''
Proper quicksort implementation
'''
def Quicksort(array, left, right):
    if left < right:
        iP = Partition(array, left, right)
        Quicksort(array, left, iP)
        Quicksort(array, iP + 1, right)

'''
Proper quicksort partition implementation
'''
def Partition(array, left, right):
    pivot = array[(left + right) // 2]
    iL = left - 1
    iR = right + 1

    while True:
        iL += 1
        while array[iL] < pivot:
            iL += 1

        iR -= 1
        while array[iR] > pivot:
            iR -= 1

        if iL >= iR:
            return iR

        array[iL], array[iR] = array[iR], array[iL]

'''
Bubble sort implementation for visualiser
Pick element at the start of the array and compare with the element next to it, repeat until the value is smaller
Repeat until sorted
'''
def VisualBubbleSort(array):
    for i in range(0, len(array)):
        swap = False
        pygame.event.pump() 
        for ii in range(0, len(array) - (1 + i)):
            # Set the colours to comparison
            array_colour[ii]     = RED
            array_colour[ii + 1] = RED
            Redraw() 

            if array[ii] > array[ii + 1]:
                array[ii], array[ii + 1] = array[ii + 1], array[ii]
                swap = True

            # Set the colours to normal
            array_colour[ii]     = WHITE
            Redraw()

        # Last element is always ordered
        array_colour[len(array) - (1 + i)] = ORANGE

        # Return if there were no swaps in the iteration.
        # Avoid wasting any more processing
        if swap == False:
            for ii in range(1, len(array)):
                pygame.event.pump()
                array_colour[ii - 1] = ORANGE
                array_colour[ii]     = GREEN
                Redraw()

            array_colour[len(array) - 1] = ORANGE
            Redraw()
            return

'''
Proper bubblesort implementation
'''
def BubbleSort(array):
    for i in range(0, len(array)):
        swap = False
        for ii in range(0, len(array) - (1 + i)):
            if array[ii] > array[ii + 1]:
                array[ii], array[ii + 1] = array[ii + 1], array[ii]
                swap = True

        # Return if there were no swaps in the iteration.
        # Avoid wasting any more processing
        if swap == False:
            return

'''
Selection sort implementation for the visualiser
Scan the array and find the smallest element in the array and add it to the start of the list
'''
def VisualSelectionSort(array):
    for i in range(0, len(array)):
        pygame.event.pump()
        iM   = i

        for ii in range(i + 1, len(array)):
            array_colour[iM] = GREEN
            array_colour[ii] = RED
            Redraw()

            if array[iM] > array[ii]:
                array_colour[iM] = WHITE
                iM = ii

            array_colour[ii] = WHITE

        if i != iM:
            array[i], array[iM] = array[iM], array[i]

        array_colour[iM] = WHITE
        array_colour[i]  = ORANGE

    for i in range(1, len(array)):
        pygame.event.pump()
        array_colour[i - 1] = ORANGE
        array_colour[i]     = GREEN
        Redraw()

'''
Proper selection sort implementation
'''
def SelectionSort(array):
    for i in range(0, len(array)):
        iM  = i
        for ii in range(i + 1, len(array)):
            if array[iM] > array[ii]:
                iM = ii

        if i != iM:
            array[i], array[iM] = array[iM], array[i]

'''
Insertion sort implementation for the visualiser
From the start of the list:
    Pick first item;
    Compare with all elements in the sorted sublist
    Shift all elements and insert the value into the correct location
    Repeat until sorted
'''
def VisualInsertionSort(array):
    for i in range(1, len(array)):
        pygame.event.pump()
        ii = i
        iL = ii - 1
        while ii > 0 and array[ii - 1] > array[ii]:
            array[ii], array[ii - 1] = array[ii - 1], array[ii]
            array_colour[ii] = WHITE
            ii -= 1
            array_colour[ii] = RED
            Redraw()

        array_colour[ii] = WHITE

    for i in range(1, len(array)):
        array_colour[i - 1] = ORANGE
        array_colour[i]     = GREEN
        Redraw()

'''
Proper insertion sort implementation
'''
def InsertionSort(array):
    for i in range(1, len(array)):
        ii = i
        while ii > 0 and array[ii - 1] > array[ii]:
            array[ii], array[ii - 1] = array[ii - 1], array[ii]
            ii -= 1

'''
Main program loop
'''
def MainLoop():
    GenerateRandomArray()
    global current_algorithm
    run = True 

    while run:
        SCREEN.fill(BLACK)

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_r:
                    GenerateRandomArray()
                elif event.key == pygame.K_RIGHT:
                    current_algorithm = (current_algorithm + 1) % len(algorithms)
                elif event.key == pygame.K_LEFT:
                    current_algorithm = (current_algorithm - 1) % len(algorithms)

                elif event.key == pygame.K_RETURN:
                    if current_algorithm == MERGE_SORT:
                        VisualMergesort(array_main, 0, len(array_main) - 1)
                    elif current_algorithm == QUICK_SORT:
                        VisualQuicksort(array_main, 0, len(array_main) - 1)
                    elif current_algorithm == BUBBLE_SORT:
                        VisualBubbleSort(array_main)
                    elif current_algorithm == SELECTION_SORT:
                        VisualSelectionSort(array_main)
                    elif current_algorithm == INSERTION_SORT:
                        VisualInsertionSort(array_main)

        Draw()
        pygame.display.update()

# Main
if __name__ == '__main__':
    MainLoop()
    pygame.quit()