# -*- coding: utf-8 -*-
'''
@File: red_packet.py
@Time: 2020/01/29 20:41:36
@Author: 大梦三千秋
@Contact: yiluolion@126.com
'''

# Put the import lib here
import random

def get_random_red_packet(total_amount, quantities):
    '''抢红包函数

    Args:
        total_amount: 红包总金额
        quantities: 红包个数

    Returns:
        返回每人领取红包的金额数
    '''
    # 用以存储每个人领取的红包金额
    amount_list = []
    # 抢红包人数
    person_num = quantities
    # 涉及红包金额可带 2 位小数部分
    # 使用先乘 100 计算，再除 100 处理小数点部分
    cur_total_amount = total_amount * 100
    # 这里采用的是二倍均值法
    # 除最后一人，先对前面领取红包金额进行处理
    # 最后剩下的金额，即是最后一人的金额
    for _ in range(quantities - 1):
        amount = random.randint(cur_total_amount // person_num, cur_total_amount // person_num * 2)
        print(amount)
        # 每次减去当前随机金额，用剩余金额进行下次随机获取
        cur_total_amount -= amount
        person_num -= 1
        amount_list.append(amount / 100)
    amount_list.append(cur_total_amount / 100)
    # print(sum(amount_list))
    return amount_list


def main():
    amount_list = get_random_red_packet(100, 33)
    for amount in amount_list:
        print('红包金额：{}'.format(amount))


if __name__ == "__main__":
    main()