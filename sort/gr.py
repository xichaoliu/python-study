#!/usr/bin/python3
#生成一定范围年限内的类身份证号脚本
import random

'''
@description 生成身份证号并输出到本地文档
@param textName - 输出文档名称
@param number - 身份证号数量
@param startYear - 开始年份
@param endYear - 结束年份
@author lxc
'''
def generateIds(textName, number, startYear, endYear):
    with open(textName, 'w') as ids:
        for index in range(1, number):
            year = random.randint(startYear, endYear)
            month = random.randint(1, 12)
            day = random.randint(1,31)

            month = month if month > 9 else '0'+str(month)
            day = day if day > 9 else '0' + str(day)
            targetBirth = str(year)+str(month) +str(day)

            prefix = random.randint(100000,666666)
            suffixList = [0,1,2,3,4,5,6,7,8,9,'x']
            suffix = str(random.randint(100, 999)) + str(suffixList[random.randint(0, 10)])

            idStr = str(prefix)+str(targetBirth) + suffix + '\n'
            ids.write(idStr)
#h.txt 两千万
# generateIds('h.txt', 10**7*2, 1900, 2021)
#s.txt 两千万
generateIds('s.txt', 10**7*2, 1900, 2021)