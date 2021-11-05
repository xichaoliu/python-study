#!/usr/bin/python3
#归并排序

# 拆分
def mergeSort(list):
    length = len(list)
    if length <=1:
        return list
    divid = length // 2
    return merge(mergeSort(list[0:divid]), mergeSort(list[divid:]))
# 归并
def merge(leftList, rightList):
    list = []
    leftPointer = 0
    rightPointer = 0
    while leftPointer < len(leftList) and rightPointer < len(rightList):
        if leftList[leftPointer]<= rightList[rightPointer]:
            list.append(leftList[leftPointer])
            leftPointer = leftPointer + 1
        else:
            list.append(rightList[rightPointer])
            rightPointer = rightPointer + 1
    while leftPointer < len(leftList):
        list.append(leftList[leftPointer])
        leftPointer = leftPointer + 1
    while rightPointer < len(rightList):
        list.append(rightList[rightPointer])
        rightPointer = rightPointer + 1
    return list