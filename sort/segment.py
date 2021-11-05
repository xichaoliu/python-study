# 大文件根据出生年份拆分成多个（这里选三个）子文件，对子文件独立排序，最后合并到一个文件中
from time import *
from main import sortFile
#读取文件
beginTime = time()
print('开始读取数据....')
fst = open('1.txt', 'w')
snd = open('2.txt', 'w')
trd = open('3.txt', 'w')
with open("s.txt") as fileObject:
    data = {}
    line = fileObject.readline()
    while line:
        line = line.strip()
        if not len(line):
            line = fileObject.readline()
            continue
        birth =  line[6:10] # 截取年龄 转换为数值字典类型，去重
        birthYear = int(birth)
        if birthYear <= 1940:
            fst.write(line + '\n')
        elif birthYear <=1980:
            snd.write(line + '\n')
        else:
            trd.write(line + '\n')
        line = fileObject.readline()
fst.close()
snd.close()
trd.close()
readEndTime = time()
print('主文件读取拆分时间：', readEndTime -beginTime)
sortFile('1.txt', '1.txt')
sortFile('2.txt', '2.txt')
sortFile('3.txt', '3.txt')
subEndTime = time()
print('子文件排序耗时：',subEndTime - readEndTime)
pathNames = ['1.txt', '2.txt', '3.txt']
with open('result.txt', 'w') as resutFile:
    for pathName in pathNames:
        with open(pathName) as subFile:
            line = subFile.readline()
            while line:
                line = line.strip()
                if not len(line):
                    line = subFile.readline()
                    continue
                resutFile.write(line + '\n')
                line = subFile.readline()
endTime = time()
print('文件合并耗时',endTime - subEndTime)
print('全程总耗时',endTime - beginTime)

# 拆分排序 {'出生日期': ['身份证号']}结构 + 两千万条数据 +  归并排序
# 内存占用峰值：606MB
# 主文件读取拆分时间： 24.882073879241943
# 子文件排序耗时： 17.99181079864502
# 文件合并耗时 17.2064311504364
# 全程总耗时 60.080315828323364

# 结论：耗时比不拆分文件久(不拆分同量级在20秒上下), 内存占用峰值低（同量级在1700~1800MB, 且持续时间相对较久）