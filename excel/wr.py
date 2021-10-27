import xlwt
import random

# 生成一定记录数量的表格
def outputExcel(lineCount, fileName):
  wb = xlwt.Workbook()
  sheetCount = 1
  ws = wb.add_sheet('Sheet' + str(sheetCount))

  lineIndex = 0
  while lineCount >= 0:
    id = random.randint(10000, 10020)
    ws.write(lineIndex, 0, id)
    ws.write(lineIndex, 1, '根据不同的id分组')
    if lineIndex >= 65535:
      sheetCount = sheetCount + 1
      ws = wb.add_sheet('Sheet' + str(sheetCount))
      lineIndex = 0
    else:
      lineIndex = lineIndex + 1
    lineCount = lineCount - 1
  wb.save(fileName)

# outputExcel(20000, '两万.xls')
outputExcel(65537, '超限.xls')