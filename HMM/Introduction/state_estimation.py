array = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

def move_forward(array):
    copy_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i, location in enumerate(array):
        if location != 0:
            if i == len(array) - 1:
                copy_array[i] += array[i]
            elif i == len(array) - 2:
                copy_array[i] += array[i] * 0.25
                copy_array[i + 1] += array[i] * 0.75
            else:
                copy_array[i] += array[i] * 0.25
                copy_array[i + 1] += array[i] * 0.50
                copy_array[i + 2] += array[i] * 0.25
    
    return copy_array

def move_backward(array):
    copy_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i, location in enumerate(array):
        if location != 0:
            if i == 0:
                copy_array[i] += array[i]
            elif i == 1:
                copy_array[i] += array[i] * 0.25
                copy_array[i - 1] += array[i] * 0.75
            else:
                copy_array[i] += array[i] * 0.25
                copy_array[i - 1] += array[i] * 0.50
                copy_array[i - 2] += array[i] * 0.25
    
    return copy_array

array = move_forward(array)
array = move_forward(array)
array = move_forward(array)
array = move_backward(array)
array = move_backward(array)
print(array)