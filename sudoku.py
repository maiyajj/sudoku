# coding=utf-8
# @File  : sudoku.py
# @Author: "maiyajj"
# @Date  : 2018/3/1
# @Desc  : 唯余法，唯一候选数法，摒除法，X-Wing法，三链数删减法，三链列删减法, 直观隐性数对，假设法
"""
数独解密脚本，手工填入待解数独，运行脚本即可输出运行结果
使用排除法进行解密
0 1 5 | 7 0 9 | 2 8 0
0 0 2 | 0 8 0 | 4 0 0
0 8 3 | 5 0 2 | 6 7 0
---------------------
9 0 0 | 1 0 7 | 0 0 6
0 3 0 | 0 0 0 | 0 2 0
5 0 0 | 8 0 3 | 0 0 1
---------------------
0 5 6 | 9 0 1 | 8 3 0
0 0 9 | 0 3 0 | 1 0 0
0 7 1 | 4 0 8 | 9 5 0
数独分为9个宫格，计算每个宫格内待填数的所有可选数并生成新表
 4679     1      5   |   7   1346    9   |   2      8     1359
 4679   4679     2   | 1346    8   1346  |   4    1359    1359
 4679     8      3   |   5   1346    2   |   6      7     1359
--------------------------------------------------------------
   9   124678 124678 |   1   24569   7   | 345789 345789    6
124678    3   124678 | 24569 24569 24569 | 345789   2   345789
   5   124678 124678 |   8   24569   3   | 345789 345789    1
--------------------------------------------------------------
 2348     5     6    |   9    2567   1   |   8      3     2467
 2348   2348    9    |  2567    3   2567 |   1     2467   2467
 2348     7     1    |   4    2567   8   |   9      5     2467
--------------------------------------------------------------
将新表内待填数4679与该行或该列进行对比去除存在数得到新值467,9为已存在数；
将每个待填数去重后得到新表；
轮询几次后即可得到数独的解。
6 1 5 | 7 4 9 | 2 8 3
7 9 2 | 3 8 6 | 4 1 5
4 8 3 | 5 1 2 | 6 7 9
---------------------
9 2 8 | 1 5 7 | 3 4 6
1 3 7 | 6 9 4 | 5 2 8
5 6 4 | 8 2 3 | 7 9 1
---------------------
2 5 6 | 9 7 1 | 8 3 4
8 4 9 | 2 3 5 | 1 6 7
3 7 1 | 4 6 8 | 9 5 2
"""
import copy
import os
import time
from collections import Counter
from itertools import combinations

__version__ = "0.0.4"

"""
Change History

Version in 0.0.4
* 三链数删减法，假设法.

Version in 0.0.3
* 直观隐性数对.

Version in 0.0.2
* 摒除法，X-Wing法，三链列删减法.

Version in 0.0.1
* 唯余法, 唯一候选数法.
"""

if os.sys.version_info[:1] < (3,):
    print("Python版本不支持，当前版本为Python%s" % os.sys.version.split("|")[0])
    os._exit(0)

# 待解数独0（最易）
sudoku0 = [[0, 1, 5, 7, 0, 9, 2, 8, 0],
           [0, 0, 2, 0, 8, 0, 4, 0, 0],
           [0, 8, 3, 5, 0, 2, 6, 7, 0],
           [9, 0, 0, 1, 0, 7, 0, 0, 6],
           [0, 3, 0, 0, 0, 0, 0, 2, 0],
           [5, 0, 0, 8, 0, 3, 0, 0, 1],
           [0, 5, 6, 9, 0, 1, 8, 3, 0],
           [0, 0, 9, 0, 3, 0, 1, 0, 0],
           [0, 7, 1, 4, 0, 8, 9, 5, 0]]

# 待解数独2（中等）
sudoku2 = [[0, 9, 0, 6, 0, 0, 7, 0, 1],
           [2, 0, 0, 0, 0, 3, 0, 8, 4],
           [7, 0, 3, 0, 0, 0, 0, 0, 0],
           [0, 3, 0, 0, 6, 1, 0, 0, 0],
           [6, 0, 0, 0, 0, 0, 0, 0, 8],
           [0, 0, 0, 9, 4, 0, 0, 7, 0],
           [0, 0, 0, 0, 0, 0, 5, 0, 2],
           [1, 5, 0, 3, 0, 0, 0, 0, 9],
           [9, 0, 6, 0, 0, 2, 0, 1, 0]]

# 待解数独3(难)
sudoku3 = [[0, 4, 3, 0, 5, 0, 0, 0, 8],
           [9, 0, 0, 8, 6, 3, 0, 2, 0],
           [1, 0, 0, 0, 0, 7, 0, 0, 0],
           [0, 1, 0, 0, 3, 0, 7, 8, 0],
           [6, 3, 0, 7, 0, 9, 0, 5, 1],
           [0, 2, 9, 0, 8, 0, 0, 4, 0],
           [0, 0, 0, 2, 0, 0, 0, 0, 3],
           [0, 9, 0, 5, 7, 4, 0, 0, 2],
           [5, 0, 0, 0, 9, 0, 4, 1, 0]]

# 待解数独1(骨灰级难度)
sudoku1 = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 3, 6, 0, 0, 0, 0, 0],
           [0, 7, 0, 0, 9, 0, 2, 0, 0],
           [0, 5, 0, 0, 0, 7, 0, 0, 0],
           [0, 0, 0, 0, 4, 5, 7, 0, 0],
           [0, 0, 0, 1, 0, 0, 0, 3, 0],
           [0, 0, 1, 0, 0, 0, 0, 6, 8],
           [0, 0, 8, 5, 0, 0, 0, 1, 0],
           [0, 9, 0, 0, 0, 0, 4, 0, 0]]

# 难
sudoku4 = ["300201009",
           "009000500",
           "060000030",
           "080502040",
           "200000007",
           "040306020",
           "030000050",
           "006000700",
           "000907003"]

# 摒除法/X-Wing法（难）
sudoku5 = ["050000020",
           "400206007",
           "008030100",
           "010000060",
           "009000500",
           "070000090",
           "005080300",
           "700901004",
           "020000070"]


# 纵向扫描数独组
def digits(sudoku):
    """
    纵向扫描传入数独组，将传入数独组横列置换，输出新数独组

    :param sudoku: 待置换数独组
    :type  sudoku: list

    :return: 横列置换的数独组
    :rtype: list
    """
    sudokus = copy.deepcopy(sudoku)  # 将原数独组拷贝一份，避免修改原数独组
    # 创建空列表
    digit = []
    for r in range(9):
        # 创建缓存空列表
        tmp = []
        for d in range(9):
            # 将原数独组每列数填至缓存列表
            tmp.append(sudokus[d][r])
        # 将缓存列表数据存入最终列表，type->[[],[]...]
        digit.append(tmp)

    return digit


# 宫格扫描数独组
def rolls(sudoku):
    """
     宫格扫描传入数独组，将传入数独组宫格置换，输出新数独组

    :param sudoku: 待置换数独组
    :type  sudoku: list

    :return: 宫格置换的数独组
    :rtype: list
    """
    sudokus = copy.deepcopy(sudoku)  # 将原数独组拷贝一份，避免修改原数独组
    # 创建空列表
    roll = []
    # 行列切片参数max:行; max1:列
    max1, max2 = 3, 3
    """
    先提取
    第1行的第1列至第3列数据，再
    第2行的第1列至第3列数据，最后
    第3行的第1列至第3列数据，填入缓存列表。
    再提取
    第1行的第1列至第4列数据，再
    第2行的第1列至第5列数据，最后
    第3行的第1列至第6列数据，填入缓存列表。
    依次提取数据，从上到下从左至右。
    """
    while max1 <= 9:
        # 创建缓存列表
        tmp1 = []
        for d in range(9):
            # max=3:第1行至第3行; max=6:第4行至第6行; max=9:第7行至第9行
            if max1 - 3 <= d < max1:
                for r in range(9):
                    # max1=3:第1列至第3列; max1=6:第4列至第6列; max1=9:第7列至第9列
                    if max2 - 3 <= r < max2:
                        # 填入缓存列表
                        tmp1.append(sudokus[d][r])
        # 缓存列表填入宫格置换列表
        roll.append(tmp1)
        max2 += 3  # 第一宫格计算完毕开始计算第二宫格（从左至右）
        # 第三宫格计算完毕转入下3列
        if max2 > 9:
            max1 += 3
            max2 = 3

    return roll


# 宫格置换的逆运算
def re_rolls(sudoku):
    """
    宫格置换的逆运算，将宫格置换后的数独组置换成原顺序数独组

    :param sudoku: 待宫格置换的数独组
    :type  sudoku: list

    :return: 原顺序数独组
    :rtype: list
    """
    return rolls(sudoku)


# 行列置换的逆运算
def re_digits(sudoku):
    """
    行列置换的逆运算，将行列置换后的数独组置换成原顺序数独组

    :param sudoku: 待行列置换的数独组
    :type  sudoku: list

    :return: 原顺序数独组
    :rtype: list
    """
    return digits(sudoku)


# 计算宫格待填数的所有可能解
def permutation_num(sudoku):
    """
    计算宫格内的待填数的所有可能解，填充至原数独组

    :param sudoku: 待置换数独组
    :type  sudoku: list

    :return: 待填数已被可能解替代的数独组
    :rtype: list
    """
    sudokus = copy.deepcopy(sudoku)  # 将原数独组拷贝一份，避免修改原数独组
    # 轮询数独组每行数据
    for r in sudokus:
        # 对比标准值
        compa = "123456789"
        # 将该行每个元素进行对比
        for i in r:
            # 若该元素在标准值内出现即删除，轮询完毕剩下待填数的所有可能值
            compa = compa.replace(i, "")
        # 将所有可能值填充至原数独组对应位置
        for index, i in enumerate(r):
            if i == "0":
                r[index] = compa
    return sudokus


# 标记所有待填数位置
def mark_posit(sudoku, signal=False):
    """
    标记所有待填数的位置信息，用字典表示，key为'00'表示数独组第一行第一列数，value为'4679',key不变，value会变

    :param sudoku: 待计算数独组
    :type  sudoku: list

    :keyword signal: 配置标记已存在数/待填数的位置。False：待填数；True：已存在数
    :type    signal: bool

    :return: 待填数和该值位置的关系字典{"00": 4679, "04": 1346}
    :rtype: dict
    """
    # 创建空字典
    position = {}
    for index, rows in enumerate(sudoku):
        for index1, row in enumerate(rows):
            # 根据数独组的每个数字值长度进行判断该位置是否需要进行计算
            if not signal:
                if len(row) != 1:
                    # 返回key为行列标识，值为可能解的 “行列位置-值” 属性字典
                    position[str(index) + str(index1)] = row
            else:
                if len(row) == 1 and row != "0":
                    # 返回key为行列标识，值为可能解的 “行列位置-值” 属性字典
                    position[str(index) + str(index1)] = row

    return position


# 唯余解法
def eliminate(sudoku):
    """
    某宫格可以添入的数已经排除了8个,那么这个宫格的数字就只能添入那个没有出现的数字。

    :param sudoku: 待解数独组
    :type  sudoku: list

    :return: 已删减待填数值可选范围的新数独组和新“行列位置-值”关系表
    :rtype: (list, dict)
    """

    # 检查数独组每行已存在数
    def check_rows():
        """
        删减每行待填数值的可选范围

        :return: 已删减待填数值可选范围的新数独组
        :rtype: list
        """
        nonlocal sudokus, posits
        # 轮询数独组
        while True:
            # 扫描前“行列位置-值”关系表
            start_posits = mark_posit(sudokus)
            for index, rows in enumerate(sudokus):
                # 已存在数列表
                signal_num = [i for i in rows if len(i) == 1]
                for index1, row in enumerate(rows):
                    # 如果数字长度不为1（发现待填数）
                    if len(row) != 1:
                        # 查找并删除该行所有重复数
                        for x in signal_num:
                            row = row.replace(x, "")
                    sudokus[index][index1] = row

            # 扫描后“行列位置-值”关系表
            posits = mark_posit(sudokus)

            if start_posits == posits or not posits:
                break

        return sudokus

    # 检查数独组每列已存在数
    def check_digits():
        """
        删减每列待填数值的可选范围

        :return: 已删减待填数值可选范围的新数独组
        :rtype: list
        """
        nonlocal sudokus
        # 将原数独组行列置换
        sudokus = digits(sudokus)
        # 删除重复数
        sudokus = check_rows()
        # 还原数独组
        sudokus = re_digits(sudokus)

        return sudokus

    # 检查数独组每宫格已存在数
    def check_rolls():
        """
        轮询每宫格已存在数

        :return: 已删减待填数值可选范围的新数独组
        :rtype: list
        """
        nonlocal sudokus
        # 宫格置换原数独组
        sudokus = rolls(sudokus)
        # 删除重复数
        sudokus = check_rows()
        # 还原数独组
        sudokus = re_rolls(sudokus)

        return sudokus

    sudokus = copy.deepcopy(sudoku)  # 将原数独组拷贝一份，避免修改原数独组
    while True:
        # 处理之前位置关系表
        start_posit = mark_posit(sudokus)
        # 检查数独组行
        sudokus = check_rows()
        # 检查数独组列
        sudokus = check_digits()
        # 检查数独组宫格
        sudokus = check_rolls()
        # 处理之后位置关系表
        posits = mark_posit(sudokus)
        # 经过行列宫格处理后待填数范围没变无法继续排除，退出
        if posits == start_posit or not posits:
            break

    return sudokus, posits


# 唯一候选数法
def singles_candidature(sudoku, posit):
    """
    使用唯一候选数法对数独组进行排除

    :param sudoku: 待填数独组
    :type  sudoku: list

    :param posit: 数独待填数值与位置关系表
    :type  posit: dict

    :return: 已删减待填数值可选范围的新数独组和新“行列位置-值”关系表
    :rtype: (list, dict)
    """
    # 位置-值表为空，表示数独已有解，返回数独解
    if not posit:
        return sudoku, {}

    def scan(way):
        """
        开始扫描

        :keyword way: 扫描方式，行/列/宫格，rows, digits, rolls
        :type    way: string
        :key     way: rows, digits, rolls

        :return: 已删减待填数值可选范围的新数独组
        :rtype: list
        """
        nonlocal sudokus, posits
        # 位置-值表为空，表示数独已有解，返回数独解
        if not posits:
            return sudokus

        # 数独组转换方式
        sudokus = sudokus if way == "rows" else digits(sudokus) if way == "digits" else rolls(sudokus)

        # 隐性唯一候选数法：当某个数字在某一列各宫格的候选数中只出现一次时，
        # 那么这个数字就是这一列的唯一候选数了
        # 扫描每行待填数中只出现一次的数字
        num_count = {}
        for index_rows, rows in enumerate(sudokus):
            # 例：第一行["12", "123", "134", "5"] -> "12123134"
            # 已存在数不计入在内
            row = "".join([i for i in rows if len(i) != 1])
            # 上例，找出每个数字出现的次数为1的值
            # num_count = {0: {2: '4'}}
            num_count[index_rows] = {[index_row for index_row, row in enumerate(rows) if key in row][0]: key
                                     for key, value in Counter(row).items() if value == 1}

        # 通过前步得到的出现次数为1值的坐标，替换至原数独组的对应位置中
        for index_rows, rows in num_count.items():
            for index_row, row in rows.items():
                sudokus[index_rows][index_row] = row

        # 还原数独组
        sudokus = sudokus if way == "rows" else re_digits(sudokus) if way == "digits" else re_rolls(sudokus)

        return sudokus

    sudokus = copy.deepcopy(sudoku)
    posits = copy.deepcopy(posit)

    while posits:
        # 列扫描
        sudokus = scan("rows")
        sudokus, start_posit = eliminate(sudokus)

        # 行扫描
        sudokus = scan("digits")
        sudokus, posits = eliminate(sudokus)
        # 扫描前后位置-值表结果相同，退出
        if start_posit == posits:
            break

    return sudokus, posits


# 摒除法
def discard(sudoku, posit):
    """
    使用行，列，宫格摒除法处理数独组。
    利用1～9的数字在每一行、每一列、每一个九宫格都只能出现一次的规则进行解题的方法。
    基础摒除法可以分为行摒除、列摒除、九宫格摒除。
    寻找九宫格摒除解：找到了某数在某一个九宫格可填入的位置只余一个的情形；意即找到了该数在该九宫格中的填入位置。
    寻找列摒除解：找到了某数在某列可填入的位置只余一个的情形；意即找到了该数在该列中的填入位置。

    :param sudoku: 待填数独组
    :type  sudoku: list

    :param posit: 数独待填数值与位置关系表
    :type  posit: dict

    :return: 已删减待填数值可选范围的新数独组和新“行列位置-值”关系表
    :rtype: (list, dict)
    """
    # 位置-值表为空，表示数独已有解，返回数独解
    if not posit:
        return sudoku, {}

    # 已存在数的位置和值
    def exist_num_posit():
        """
        已存在数的所有值（已经去除重复的），例“1和2和3”。和存在数的所有存在位置

        :return: 存在数的位置，和所有值
        :rtype: (dict， string)
        """
        nonlocal sudokus
        # 从已填数列表得到所有代已填数的位置集合
        # {'0': ['00', '01', '34'...], '1':[...]...}
        signal_posit_list = {}
        signal_posit = mark_posit(sudokus, True)
        for k, v in signal_posit.items():
            if v not in signal_posit_list:
                signal_posit_list[v] = []
            signal_posit_list[v].append(k)

        for i in range(1, 10):
            if str(i) not in signal_posit_list:
                signal_posit_list[str(i)] = []

        # 存在数的值
        # 所有数字的合集，存在1234或3245等
        wait_search = ["".join([i for i in rows if len(i) != 1 or i != "0"]) for rows in sudokus]
        wait_search = "".join(set("".join(wait_search)))

        return signal_posit_list, wait_search

    # 扫描
    def scan(way):
        """
        开始扫描

        :keyword way: 扫描方式，行/列/宫格，rows, digits, rolls
        :type    way: string

        :return: 已删减待填数值可选范围的新数独组和新“行列位置-值”关系表
        :rtype: list
        """
        nonlocal sudokus, posits
        # 位置-值表为空，表示数独已有解，返回数独解
        if not posits:
            return sudokus

        signal_posit_list, wait_search = exist_num_posit()

        for num in wait_search:
            # 若某宫格存在该数字，则宫格其他待填处均可排除，用R代替
            tmp_su = rolls(sudokus)
            for index, rows in enumerate(tmp_su):
                # 待填数暂用0表示
                for index1, row in enumerate(rows):
                    if len(row) != 1:
                        tmp_su[index][index1] = "0"
                # 若该宫格存在数字num，宫格其他处用R替换
                if num in rows:
                    tmp_su[index] = ".".join(rows).replace("0", "R").split(".")
            tmp_su = re_rolls(tmp_su)

            # 若某行列存在该数字，则行列其他待填处均可排除，用R代替
            for x, y in signal_posit_list[num]:
                for index, rows in enumerate(tmp_su):
                    # 若该行存在数字num，该行其他处用R替换
                    if index == int(x):
                        tmp_su[index] = ".".join(rows).replace("0", "R").split(".")
                    # 若该列存在数字num，该列其他处用R替换
                    if tmp_su[index][int(y)] == "0":
                        tmp_su[index][int(y)] = "R"

            # 数独组转换方式
            tmp_su = tmp_su if way == "rows" else digits(tmp_su) if way == "digits" else rolls(tmp_su)

            # 找出只能填该num数字可填入的位置只余一个
            # 使用X代替
            for index, rows in enumerate(tmp_su):
                if rows.count("0") == 1:
                    tmp_su[index] = ".".join(rows).replace("0", "X").split(".")

            # 还原数独组
            tmp_su = tmp_su if way == "rows" else re_digits(tmp_su) if way == "digits" else re_rolls(tmp_su)

            # 在还原数独组内找出所有X的位置
            x_posit = [str(index) + str(index1) for index, rows in enumerate(tmp_su)
                       for index1, row in enumerate(rows) if row == "X"]

            # 将num数值写入X的位置
            for x, y in x_posit:
                sudokus[int(x)][int(y)] = num

        return sudokus

    sudokus = copy.deepcopy(sudoku)  # 将原数独组拷贝一份，避免修改原数独组
    posits = copy.deepcopy(posit)

    while posits:
        # 行扫描
        sudokus = scan("rows")
        sudokus, start_posits = eliminate(sudokus)

        # 列扫描
        sudokus = scan("digits")
        sudokus, posits = eliminate(sudokus)

        # 宫格扫描
        sudokus = scan("rolls")
        sudokus, posits = eliminate(sudokus)

        # 无法继续处理则退出摒除法处理
        if start_posits == posits:
            break

    return sudokus, posits


# X-Wing法
def xwing(sudoku, posit):
    """
    X-Wing,在中文叫矩形摒除（或矩形删减）。在日本则叫四角对角线之原理。

    :param sudoku: 待填数独组
    :type  sudoku: list

    :param posit: 数独待填数值与位置关系表
    :type  posit: dict

    :return: 已删减待填数值可选范围的新数独组和新“行列位置-值”关系表
    :rtype: (list, dict)
    """
    # 位置-值表为空，表示数独已有解，返回数独解
    if not posit:
        return sudoku, {}

    # x-wing坐标
    def get_x_wing_posit(vx, v):
        # 该行/列数只存在2个候选数
        vv = [x + y for x, y in v if vx.count(x) == 2]
        # TODO: 忘了是干嘛的，添加注释
        vv = vv if len(vv) % 4 == 0 and vv else ""

        # 该候选数所在行列
        num = "".join(set([x for x, y in vv]))
        # 得到该数字可以组成X-Wing的所有可能解
        vv = [[x + y for x, y in vv if x == i] for i in num]
        vv = [i for i in vv if len(i) == 2 and len(vv) % 2 == 0]

        tmp = []
        for value in vv:
            # X-Wing值要求4个组只在两行和两列，即X相等，Y相等
            y = value[0][1] + value[1][1]
            tmp1 = []
            for i in vv:
                if y == i[0][1] + i[1][1]:
                    tmp1.append(i)
            tmp1 = sum(tmp1, [])
            # 输出所有解[[12, 23, 32, 33], [35, 36, 75, 76]...],etc
            if tmp1 not in tmp and len(tmp1) == 4:
                tmp.append(tmp1)

        return tmp

    # 返回X-Wing数字组合
    def get_coord():
        """
        获取可以组成X-Wing法的数字和该数字坐标

        :return: 该数字和数字坐标字典
        :rtype: dict
        """
        nonlocal posits, xwing_result

        # 从待填数列表得到所有待填数的位置集合
        # {'0': ['00', '01', '34'...], '1':[...]...}
        wait_posit = {}
        for k, v in posits.items():
            for i in v:
                if i not in wait_posit:
                    wait_posit[i] = []
                wait_posit[i].append(k)

        # 计算数独组内可以组成X-Wing法的数字和该数字坐标
        for k, v in wait_posit.items():
            # 通过行寻找X-Wing数字
            vx = [x for x, y in v]  # 所有数字所在行数
            vx = get_x_wing_posit(vx, v)
            # 通过列寻找X-Wing数字
            vy = [y for x, y in v]  # 所有数字所在列数
            vy = get_x_wing_posit(vy, v)

            xwing_result[k] = vx + vy
            if not vx and not vy:
                xwing_result.pop(k)

        return xwing_result

    xwing_result = {}
    sudokus = copy.deepcopy(sudoku)
    posits = copy.deepcopy(posit)

    # 获取X-Wing数字组合
    coord = get_coord()
    for num, coord_posit in coord.items():
        for iii in coord_posit:
            # 通过行查找
            x = set([x for x, y in iii])
            # 通过列查找
            y = set([y for x, y in iii])
            for su_posit, value in posits.items():
                for xx in x:
                    # 该行其他待填数全部删除当前当前值，缩减可选数范围
                    if xx == su_posit[0] and su_posit not in iii:
                        posits[su_posit] = value.replace(num, "")
                for yy in y:
                    # 该列其他待填数全部删除当前当前值，缩减可选数范围
                    if yy == su_posit[1] and su_posit not in iii:
                        posits[su_posit] = value.replace(num, "")

    # 更新数独组可选值
    for k, v in posits.items():
        x, y = k
        sudokus[int(x)][int(y)] = v

    sudokus, posits = eliminate(sudokus)

    return sudokus, posits


# 三链数删减法
def naked_triples(sudoku, posit):
    """
    找出某一列、某一行或某一个九宫格中的某三个宫格候选数中，相异的数字不超过3个的情形，
    进而将这3个数字自其它宫格的候选数中删减掉的方法就叫做三链数删减法。

    :param sudoku: 待填数独组
    :type  sudoku: list

    :param posit: 数独待填数值与位置关系表
    :type  posit: dict

    :return: 已删减待填数值可选范围的新数独组和新“行列位置-值”关系表
    :rtype: (list, dict)
    """
    if not posit:
        return sudoku, {}

    def scan(way):
        """
        开始扫描

        :keyword way: 扫描方式，行/列/宫格，rows, digits, rolls
        :type    way: string
        """
        nonlocal sudokus, posits
        if not posits:
            return sudokus

        # 数独组转换方式
        sudokus = sudokus if way == "rows" else digits(sudokus) if way == "digits" else rolls(sudokus)

        # 三链数，四链数
        for num in range(2, 5):
            for index, rows in enumerate(sudokus):
                group = combinations([i for i in rows if len(i) != 1], num)
                for i in group:
                    repeat_num = set("".join(i))
                    if len(repeat_num) == num:
                        for index1, row in enumerate(rows):
                            tmp = set(row) - repeat_num
                            sudokus[index][index1] = "".join(tmp) if tmp else row

        # 还原数独组
        sudokus = sudokus if way == "rows" else re_digits(sudokus) if way == "digits" else re_rolls(sudokus)

        return sudokus

    sudokus = copy.deepcopy(sudoku)
    posits = copy.deepcopy(posit)
    while posits:
        # 行扫描
        sudokus = scan("rows")
        sudokus, start_posits = eliminate(sudokus)

        # 列扫描
        sudokus = scan("digits")
        sudokus, posits = eliminate(sudokus)

        # 宫格扫描
        sudokus = scan("rolls")
        sudokus, posits = eliminate(sudokus)

        if start_posits == posits:
            break

    return sudokus, posits


# 三链列删减法
def chain_column(sudoku, posit):
    """
    利用“找出某个数字在某三列仅出现在相同三行的情形，进而将该数字自这三行其他宫格候选数中删减掉”；
    或“找出某个数字在某三行仅出现在相同三列的情形，进而将该数字自这三列其他宫格候选数中删减掉”的方法就叫做三链列删减法
    # 算法同X-Wing法

    :param sudoku: 待填数独组
    :type  sudoku: list

    :param posit: 数独待填数值与位置关系表
    :type  posit: dict

    :return: 已删减待填数值可选范围的新数独组和新“行列位置-值”关系表
    :rtype: (list, dict)
    """
    # 位置-值表为空，表示数独已有解，返回数独解
    if not posit:
        return sudoku, {}

    # 三链列坐标
    def get_chain_column_posit(vx, v):
        nonlocal digits_num
        # 当前行/列 数小于指定值digits_num，三链列就为3，四链列就为4
        vv = [x + y for x, y in v if vx.count(x) <= digits_num]

        # 该候选数所在行列
        vv = [[x + y for x, y in vv if x == i] for i in "".join(set([x for x, y in vv]))]

        # 所有可选数排列组合后选择可能值
        vv = [sum(list(ii), []) for ii in list(combinations(vv, digits_num)) if
              len(set([y for i in ii for x, y in i])) <= digits_num]

        return vv

    # 返回三链列数字组合
    def get_coord():
        """
        获取可以组成三链列组合的数字和该数字坐标

        :return: 该数字和数字坐标字典
        :rtype: dict
        """
        nonlocal chain_column_result, posits, digits_num
        # 从待填数列表得到所有待填数的位置集合
        # {'0': ['00', '01', '34'...], '1':[...]...}
        wait_posit = {}
        for k, v in posits.items():
            for i in v:
                if i not in wait_posit:
                    wait_posit[i] = []
                wait_posit[i].append(k)

        for k, v in wait_posit.items():
            # 通过行查找
            vx = [x for x, y in v]
            # 通过列查找
            vy = [y for x, y in v]
            vx = get_chain_column_posit(vx, v)
            vy = get_chain_column_posit(vy, v)
            chain_column_result[k] = vx + vy
            if not vx and not vy:
                chain_column_result.pop(k)

        return chain_column_result

    sudokus = copy.deepcopy(sudoku)
    posits = copy.deepcopy(posit)

    # 三链列
    for digits_num in range(3, 4):
        chain_column_result = {}
        coord = get_coord()
        for num, coord_posit in coord.items():
            for iii in coord_posit:
                x = set([x for x, y in iii])
                y = set([y for x, y in iii])
                for su_posit, value in posits.items():
                    for xx in x:
                        # 该行其他待填数全部删除当前当前值，缩减可选数范围
                        if xx == su_posit[0] and su_posit not in iii:
                            posits[su_posit] = value.replace(num, "")
                    for yy in y:
                        # 该列其他待填数全部删除当前当前值，缩减可选数范围
                        if yy == su_posit[1] and su_posit not in iii:
                            posits[su_posit] = value.replace(num, "")

        for k, v in posits.items():
            x, y = k
            sudokus[int(x)][int(y)] = v

        sudokus, posits = eliminate(sudokus)

    return sudokus, posits


# 直观隐性数对
def hidden_pairs(sudoku, posit):
    """
    直观隐性数对（数组）的原理是利用数对（数组）运用排除，得到某个区域内出现一个数对（数组）占据2（3）个单元格，
    再利用其它数字的排除法解题

    :param sudoku: 待填数独组
    :type  sudoku: list

    :param posit: 数独待填数值与位置关系表
    :type  posit: dict

    :return: 已删减待填数值可选范围的新数独组和新“行列位置-值”关系表
    :rtype: (list, dict)
    """
    # 位置-值表为空，表示数独已有解，返回数独解
    if not posit:
        return sudoku, {}

    def scan(way):
        nonlocal sudokus, posits
        # 位置-值表为空，表示数独已有解，返回数独解
        if not posits:
            return sudokus

        # 数独组转换方式
        sudokus = sudokus if way == "rows" else digits(sudokus) if way == "digits" else rolls(sudokus)

        num_count = {}
        for count in range(2, 5):
            for index, rows in enumerate(sudokus):
                # 例：第一行["12", "123", "134", "5"] -> "12123134"
                # 已存在数不计入在内
                row = "".join([i for i in rows if len(i) != 1])
                num_count[index] = {}
                for key, value in Counter(row).items():
                    if value == count:
                        num_count[index][key] = []
                        for index1, i in enumerate(rows):
                            if key in i:
                                num_count[index][key].append(str(index) + str(index1))
                if len(num_count[index]) != count:
                    num_count[index] = {}
                tmp = {}
                for k, v in num_count.items():
                    for k1, i in v.items():
                        for k2, ii in v.items():
                            if i == ii and k1 != k2:
                                tmp = {"".join([k2, k1]): i}
                                # for iii in i:
                                #     x, y = iii
                                # sudokus[int(x)][int(y)] = k1
                for k, v in tmp.items():
                    if len(k) == count:
                        for i in v:
                            x, y = i
                            sudokus[int(x)][int(y)] = k
        # 还原数独组
        sudokus = sudokus if way == "rows" else re_digits(sudokus) if way == "digits" else re_rolls(sudokus)

        return sudokus

    sudokus = copy.deepcopy(sudoku)
    posits = copy.deepcopy(posit)
    while posits:
        # 行扫描
        sudokus = scan("row")
        sudokus, start_posit = eliminate(sudokus)

        # 列扫描
        sudokus = scan("digits")
        sudokus, posits = eliminate(sudokus)

        if start_posit == posits:
            break

    return sudokus, posits


# 假设法
def hypothesis(sudoku, posit):
    # 位置-值表为空，表示数独已有解，返回数独解
    if not posit:
        return sudoku

    # 找出目前没有被赋值的位置，若全部都被填满，则返回False
    def find_empty_location():
        nonlocal posits
        for row in range(9):
            for col in range(9):
                if len(sudokus[row][col]) != 1:
                    posits = str(row) + str(col)
                    return True
        return False

    # 找出num在该arr的row行是否出现过
    def used_in_row(row, num):
        nonlocal sudokus
        for i in range(9):
            if sudokus[row][i] == num:
                return True
        return False

    # 找出num在该arr的col列是否出现过
    def used_in_col(col, num):
        nonlocal sudokus
        for i in range(9):
            if sudokus[i][col] == num:
                return True
        return False

    # 找出num在该arr的3x3-box是否出现过，更应注意的是，传参技巧！
    def used_in_box(row, col, num):
        nonlocal sudokus
        for i in range(3):
            for j in range(3):
                if sudokus[row + i][col + j] == num:
                    return True
        return False

    def check_location_is_safe(row, col, num):
        return not used_in_row(row, num) and not used_in_col(col, num) and not used_in_box(row - row % 3,
                                                                                           col - col % 3, num)

    def scan(posit):
        nonlocal posits
        # get_next = min(posits, key=lambda x: len(posits[x]))

        # 找出还未被填充的位置
        if not find_empty_location():
            return True
        # 未被填充的位置，赋值给row，col
        row, col = posits
        row, col = int(row), int(col)
        for num in posit[posits]:
            if check_location_is_safe(row, col, num):
                sudokus[row][col] = num
                if scan(posit):
                    return True
                # 若当前num导致未来并没有结果，则当前所填充的数无效，置0后选下一个数测试
                sudokus[row][col] = "00"

        return False

    # 当前搜索的第几行、第几列
    sudokus = copy.deepcopy(sudoku)
    posits = copy.deepcopy(posit)
    scan(posit)
    return sudokus


# 计算解
def create_sudoku(sudoku):
    """
    根据算法求最终解

    :param sudoku: 待填数独组
    :type  sudoku: list

    :return: 最终数独解
    :rtype: list
    """
    # 将数独组每个元素转换为字符串
    if isinstance(sudoku[0], str):
        sudokus = [list(i) for i in sudoku]
    else:
        sudokus = [list(map(lambda x: str(x), i)) for i in sudoku]
    # 计算每个宫格元素的所有可选数
    sudokus = re_rolls(permutation_num(rolls(sudokus)))

    # 唯余解法
    sudokus, posits = eliminate(sudokus)
    # 唯一候选数法
    sudokus, posits = singles_candidature(sudokus, posits)
    # 宫格摒除法计算数独组
    sudokus, posits = discard(sudokus, posits)
    # X-Wing法
    sudokus, posits = xwing(sudokus, posits)
    # 三链列删减法
    sudokus, posits = chain_column(sudokus, posits)
    # 直观隐性数对
    sudokus, posits = hidden_pairs(sudokus, posits)
    # 三链数删除法
    sudokus, posits = naked_triples(sudokus, posits)
    # 假设法
    sudokus = hypothesis(sudokus, posits)
    # 格式化打印输出值
    for index1, i in enumerate(sudokus):
        for index, r in enumerate(i):
            if index == 8:
                print(r)
            elif (index + 1) % 3 == 0:
                print(r + " |", end=" ")
            else:
                print(r, end=" ")
        if (index1 + 1) % 3 == 0 and index1 != 8:
            print("---------------------")
    return sudokus


start = time.time()
end_sudoku = create_sudoku(sudoku1)
end = time.time()
print("程序运行时间：%.4fS" % (end - start))
# input("按下任意键退出脚本...")

"""
sudoku0
6 1 5 | 7 4 9 | 2 8 3
7 9 2 | 3 8 6 | 4 1 5
4 8 3 | 5 1 2 | 6 7 9
---------------------
9 2 8 | 1 5 7 | 3 4 6
1 3 7 | 6 9 4 | 5 2 8
5 6 4 | 8 2 3 | 7 9 1
---------------------
2 5 6 | 9 7 1 | 8 3 4
8 4 9 | 2 3 5 | 1 6 7
3 7 1 | 4 6 8 | 9 5 2

sudoku1
8 1 2 | 7 5 3 | 6 4 9
9 4 3 | 6 8 2 | 1 7 5
6 7 5 | 4 9 1 | 2 8 3
---------------------
1 5 4 | 2 3 7 | 8 9 6
3 6 9 | 8 4 5 | 7 2 1
2 8 7 | 1 6 9 | 5 3 4
---------------------
5 2 1 | 9 7 4 | 3 6 8
4 3 8 | 5 2 6 | 9 1 7
7 9 6 | 3 1 8 | 4 5 2

sudoku2
4 9 8 | 6 2 5 | 7 3 1
2 6 5 | 7 1 3 | 9 8 4
7 1 3 | 8 9 4 | 2 5 6
---------------------
8 3 7 | 2 6 1 | 4 9 5
6 4 9 | 5 3 7 | 1 2 8
5 2 1 | 9 4 8 | 6 7 3
---------------------
3 7 4 | 1 8 9 | 5 6 2
1 5 2 | 3 7 6 | 8 4 9
9 8 6 | 4 5 2 | 3 1 7

sudoku3
2 4 3 | 9 5 1 | 6 7 8
9 5 7 | 8 6 3 | 1 2 4
1 8 6 | 4 2 7 | 9 3 5
---------------------
4 1 5 | 6 3 2 | 7 8 9
6 3 8 | 7 4 9 | 2 5 1
7 2 9 | 1 8 5 | 3 4 6
---------------------
8 7 4 | 2 1 6 | 5 9 3
3 9 1 | 5 7 4 | 8 6 2
5 6 2 | 3 9 8 | 4 1 7

sudoku4
3 5 8 | 2 4 1 | 6 7 9
4 7 9 | 6 8 3 | 5 1 2
1 6 2 | 7 5 9 | 4 3 8
---------------------
6 8 3 | 5 7 2 | 9 4 1
2 9 5 | 8 1 4 | 3 6 7
7 4 1 | 3 9 6 | 8 2 5
---------------------
9 3 7 | 4 2 8 | 1 5 6
8 2 6 | 1 3 5 | 7 9 4
5 1 4 | 9 6 7 | 2 8 3

sudoku5
1 5 7 | 4 9 8 | 6 2 3
4 9 3 | 2 1 6 | 8 5 7
2 6 8 | 5 3 7 | 1 4 9
---------------------
5 1 4 | 3 2 9 | 7 6 8
6 8 9 | 1 7 4 | 5 3 2
3 7 2 | 8 6 5 | 4 9 1
---------------------
9 4 5 | 7 8 2 | 3 1 6
7 3 6 | 9 5 1 | 2 8 4
8 2 1 | 6 4 3 | 9 7 5
 """
