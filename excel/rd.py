import xlrd
import xlwt

'''
@description 依照每个excel表格的第n列字段合并excel表格的第一个工作表
@param targetFile 目标文件目录
@param classifyColumn 归类列 0,1,2...
@param files 要合并的文件目录列表
'''
def combineExcel(targetFile, classifyColumn, *files):
    repeatData = {}
    #读数据
    for file in files:
        book = xlrd.open_workbook(file)
        sh = book.sheet_by_index(0)
        for rx in range(sh.nrows):
            rdata=sh.row_values(rx)
            key = rdata[classifyColumn]
            if key in repeatData:
                repeatData[key].append(rdata)
            else:
                repeatData[key] = [rdata]
    # 定义间隔样式
    styleF = xlwt.XFStyle()
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 10
    styleF.pattern = pattern

    styleN = xlwt.XFStyle()
    pattern1 = xlwt.Pattern()
    pattern1.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern1.pattern_fore_colour = 11
    styleN.pattern = pattern1
    # 创建excel表格
    wb = xlwt.Workbook()
    sheetNum = 0
    ws = wb.add_sheet('sheet'+ str(sheetNum))
    index = 1
    style = styleN
    keyList = list(repeatData.keys())
    # quickSort(keyList, 0, len(keyList) - 1) # 快排 仅对数值型id有效
    # 写数据
    for key in keyList:
        style = styleF if style == styleN else styleN
        for a in range(len(repeatData[key])):
            row = repeatData[key][a]
            for column in range(len(row)):
                ws.write(index, column, row[column], style)
            if index >= 65535:
                sheetNum = sheetNum + 1
                ws = wb.add_sheet('sheet'+ str(sheetNum))
                index = 1
            else:
                index = index + 1
    wb.save(targetFile)

# example
combineExcel('result.xls', 0,'五万.xls', '一千五.xls')