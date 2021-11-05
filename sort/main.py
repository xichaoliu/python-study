#!/usr/bin/python3
# author: lxc
# 思路：读取文件 - 抽取数据 - 排序（快排/归并） - 输出文件
#分析：基于出生年月对身份证号排序，需要截取出生日期并建立出生日期与身份证号的映射关系，
#因此需要字段数据结构来维护映射关系，列表结构进行排序

import mergeSort
from time import *
import sys
import os
from quickSort import quickSort

def sortFile(inputFile, outputFile):
    #读取文件
    beginTime = time()
    print('开始读取数据....')
    with open(inputFile) as fileObject:
        data = {}
        # for line in fileObject.readlines():
        #     line = line.strip()
        #     if not len(line):
        #         continue
        #     birth =  line[6:14] # 截取年龄 转换为数值字典类型，去重
        #     key = int(birth)
        #     data[key] = data[key] + '\n' + line if key in data else line
        line = fileObject.readline()
        while line:
            line = line.strip()
            if not len(line):
                line = fileObject.readline()
                continue
            birth =  line[6:14] # 截取年龄 转换为数值字典类型，去重
            key = int(birth)
            if key in data:
                # data[key] = data[key] + '\n' + line
                data[key].append(line)
            else:
                data[key] = [line]
            line = fileObject.readline()
    readTime = time()
    print('数据读取处理时间：', readTime - beginTime)
    # print('操作数据', data, '\n')
    # 数据排序与处理
    sortList = list(data.keys())
    print('排序数据长度', len(sortList))
    sortStartTime = time()
    sortedList = mergeSort.mergeSort(sortList)
    # quickSort(sortedList, 0, len(sortedList) - 1)
    sortEndTime = time()
    print('排序时间：', sortEndTime - sortStartTime)
    # print('排序后数据', sortedList)
    # result = []
    # 输出文件
    writeTime = time()
    with open(outputFile, "w") as fo:
        for item in sortedList:
            fo.write('\n'.join(data[item]) + '\n')
    endTime = time()
    print('数据输出时间：', endTime - writeTime)
    runTime = endTime - beginTime
    print('总时间：', runTime)

# sortFile('s.txt', 'foo.txt')
# 不同字典结构 + 数量级排序性能统计 
# 执行环境：win10 + coreI7 + 8G内存
# 语言版本：python3
# 时间单位：s

# {'出生日期': '身份证号'}结构 + 六百万条数据 + 归并排序 耗时统计
# 数据读取处理时间： 11.26829195022583
# 排序时间： 0.19152235984802246
# 数据输出时间：1.594839096069336
# 总时间： 13.126460790634155

# {'出生日期': '身份证号'}结构 + 两千万条数据 +  归并排序 耗时统计
# 数据读取处理时间： 47.40061688423157
# 排序数据长度 45384 - *122年 12个月/年 31天/月 的条件下，出生日期有且仅有45384种可能，这一点体现了去重的价值，尤其在大数量级条件下*
# 排序时间： 0.19052767753601074
# 数据输出时间： 5.272495985031128
# 总时间： 53.00223350524902


# {value: '出生日期', key: '身份证号'}结构 + 两千万条数据 + 归并排序 耗时统计
# 数据读取处理时间： 26.11942148208618
# 排序数据长度 19999999
# 排序时间： 257.3885381221771
# 数据输出时间： 5.956634283065796
# 总时间： 485.26272463798523

# {'出生日期': '身份证号'}结构 + 20亿条数据(文件大小2G) +  归并排序 耗时统计
# 数据读取处理时间： 1749.5067403316498 ~ 30分钟
# 排序数据长度 45384
# 排序时间： 0.19744372367858887
# 数据输出时间： 95.64691472053528
# 总时间： 1847.3216469287872

#结论：{'出生日期': '身份证号'}形式在前期读取处理数据上会比较耗时，但因做了去重处理
#排序数据量级减少，耗时降低，总体效率占优，同时在编程上无需对排序算法做适配，通用性强
#在排序算法上，快排会比归并快几十毫秒。

#优化：数据读取处理和数据输出在亿级数据量下耗时可观，在文件读取和数据结构选择上仍有优化空间
#对于读取的优化：可换用file.readline()逐行读取，节约内存
#对于数据接口的优化，改为{'出生日期': ['身份证号']}；去重时对字符串的读取/拼接/重新写入很耗时，改为往数组中追加更为高效

# {'出生日期': ['身份证号']}结构 + 两千万条数据 +  归并排序 耗时统计
# 内存占用峰值：1785MB ~ 1.7G
# 数据读取处理时间： 20.25001549720764
# 排序数据长度 45384
# 排序时间： 0.18513798713684082
# 数据输出时间： 2.648847818374634
# 总时间： 23.084963083267212

# 统计数据：纯读取两千万条数据平均耗时6s，首次读取耗时12s