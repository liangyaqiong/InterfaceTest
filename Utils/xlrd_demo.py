import  xlrd
from Config import settings
import os


class  Excel_Data_Get:

    def __init__(self):
        self.file_name = os.path.join(settings.data_path,'test_data.xlsx')
        self.excel = xlrd.open_workbook(self.file_name)
        self.sheet =self.excel.sheet_by_name('Sheet1')

    def zuoye_one(self):
        "根据在github上的实例excel文件，利用xlrd模块读取第2列的所有数据"
        print(self.sheet.col_values(colx=1))
        print(self.sheet.row_values(0))
        print(self.sheet.row(0))

    # def zuoye_two(self,x,y):
    #    "根据在github上的实例excel文件，编写一个方法，方法参数为单元格的坐标（x,y），如果给的坐标是合并的单元格，输出此单元格是合并的，否则，输出普通单元格"
    #    merged = self.sheet.merged_cells
    #    print(merged)
    #    i = 0
    #    for rlow, rhigh, clow, chigh in merged:
    #        if rlow <= x and rhigh>x:
    #           if clow <= y and chigh >y:
    #               i = i+1
    #    if i>0:
    #        print(self.sheet.cell_value(x,y),"是合并单元格子")
    #    else:
    #        print(self.sheet.cell_value(x, y), "是普通单元格子")


    def zuoye_two(self,x,y):
       "根据在github上的实例excel文件，编写一个方法，方法参数为单元格的坐标（x,y），如果给的坐标是合并的单元格，输出此单元格是合并的，否则，输出普通单元格"
       merged = self.sheet.merged_cells
       print(merged)
       for rlow, rhigh, clow, chigh in merged:
           if rlow <= x and rhigh>x:
              if clow <= y and chigh >y:
                  print(self.sheet.cell_value(x, y), "是合并单元格子")
                  break;
           else:
               print(self.sheet.cell_value(x, y), "是普通单元格子")

    # def zuoye_two(self, x, y):
    #     "根据在github上的实例excel文件，编写一个方法，方法参数为单元格的坐标（x,y），如果给的坐标是合并的单元格，输出此单元格是合并的，否则，输出普通单元格"
    #     merged = self.sheet.merged_cells
    #     print(merged)
    #     i = 0
    #     for rlow, rhigh, clow, chigh in merged:
    #         if rlow <= x and rhigh > x:
    #             if clow <= y and chigh > y:
    #                return  print('合并')
    #     return   print('普通')
    #
    def default_excel(self):
        dict = {'name':'xiaomao','age':10}
        list = {1,2,3,4,4}

        dict.setdefault(list['测试用例编号'], []).append(list)
        return list


    def zuoye_three(self):
       "把完成情况这一列数据改为60、90、100、40，用xlrd模块取出来之后，进行降序排序输出"
       list  =  self.sheet.col_values(colx=3,start_rowx=1)
       list2 = []
       for ele in list:
           if ele != '':
               element = int(ele)
               list2.append(element)
       list2.sort(reverse=True)
       print(list2)

date = Excel_Data_Get()
date.zuoye_one()
date.zuoye_two(3,3)
date.zuoye_three()
date.default_excel()