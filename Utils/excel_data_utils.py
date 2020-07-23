import os

import xlrd
from Config import  settings

class Excel_Utils:

    def __init__(self,file_path,sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.sheet = self.get_sheet()

    def get_sheet(self):
        '取出需要读取的sheet'
        self.wb = xlrd.open_workbook(self.file_path)
        self.sheet = self.wb.sheet_by_name(self.sheet_name)
        return self.sheet

    def get_max_row(self):
        '取出最大行数'
        max_row = self.sheet.nrows
        return max_row

    def get_max_cloumn(self):
        '取出最大列数'
        max_column= self.sheet.ncols
        return max_column

    def get_cell_value(self,row_index,column_index):
        '简单根据坐标取出一个单元格的值'
        cell_value = self.sheet.cell_value(row_index,column_index)
        return cell_value

    def get_merge_cell(self):
        "找出excel的合并单元格，返回一个列表"
        merge_cell = self.sheet.merged_cells
        return merge_cell

    def get_merge_cell_value(self,row_index,column_index):
        "处理excell数据，将每个cell的值取出来，主要实现了合并单元格的处理"
        for rlow, rhigh, clow, chigh in self.get_merge_cell():
            if rlow <= row_index and rhigh > row_index:
                if clow <= column_index and chigh > column_index:
                    cell_value = self.get_cell_value(rlow,clow)
                    break;
                else:
                   cell_value =  self.get_cell_value(row_index,column_index)
            else:
                cell_value = self.get_cell_value(row_index, column_index)

        return cell_value


    def get_dict_data(self):
         "将excel数据每一行作为一个字典取出来存放在类表中"
         list_data =[]
         for row in range(1,self.get_max_row()):
             row_dict = {}
             row_head = self.sheet.row_values(0)
             for column in range(0,self.get_max_cloumn()):
                 row_dict[row_head[column]] = self.get_merge_cell_value(row,column)

             list_data.append(row_dict)

         return  list_data


if __name__ == '__main__':

    excel =Excel_Utils(os.path.join(settings.data_path, 'test_case.xlsx'),'Sheet1')
    for ele in excel.get_dict_data():
        print(ele)
