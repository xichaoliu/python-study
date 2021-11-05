#!/usr/bin/python3
# 分治
def quickSort(list, left, right):
    if len(list) <= 1:
        return
    index = partition(list, left, right)
    if left < index - 1:
        quickSort(list, left, index -1)
    if right > index:
        quickSort(list, index, right)

# 排序
def partition(list, left, right):
    baseNumber = list[(left + right ) // 2]
    i = left
    j = right
    while i <= j:
        while list[i] < baseNumber:
            i = i + 1
        while list[j] > baseNumber:
            j = j - 1
        if i <= j:
            temp = list[i]
            list[i] = list[j]
            list[j] = temp
            i = i+1
            j = j-1
    return i