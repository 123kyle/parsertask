#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import pandas as pd
import click

from models import Task

col_map = {
    2: "任务名称",
    5: "需求编号",
    6: "主测试",
    7: "测试",
    15: "功能测试开始时间",
    16: "功能测试结束时间",
    19: "内部联调开始时间",
    20: "内部联调结束时间",
    23: "商家联调开始时间",
    24: "商家联调结束时间"
}

colors = {1: '#FF4500',  # 功能
          2: '#DB7093',  # 内部连调
          3: '#DA70D6',  # 商家
          10: "#A9A9A9"}


def style_apply(series, colors, back_ground=''):
    """
    :param series: 传过来的数据是DataFramt中的一列   类型为pd.Series
    :param colors: 内容是字典  其中key 为标题名   value 为颜色
    :param back_ground: 北京颜色
    :return:
    """
    return ['background-color: %s' % (colors.get(item)) for item in series]


def convert_time(data):
    try:
        return data.to_pydatetime()
    except:
        pass


def create_data_frame(tasks, start, end):
    rows = []

    for item in tasks:
        row = item.to_list(start, end)
        rows.append(row)
    step = datetime.timedelta(days=1)
    days = [(start + (i * step)).date() for i in range((end - start).days + 1)]
    cols = ["主测试", "测试", "任务名称", "需求编号"] + days
    df = pd.DataFrame(rows, columns=cols)
    return df


@click.command()
@click.option('--dst', default="default.xlsx")
@click.option('--srt')
def main(srt, dst):
    if not os.path.exists(srt):
        print("could not found {}".format(srt))
        return

    execl_file = srt
    writer = pd.ExcelFile(execl_file)
    data_frame = writer.parse("商家维度任务列表")
    all_tasks = []
    max_time = datetime.datetime.now()
    min_time = datetime.datetime.now()
    for index, rows in data_frame.iterrows():
        name = rows[2]
        no = rows[5]
        main_tester = rows[6]
        support_tester = rows[7]
        func_start_time = convert_time(rows[15])
        func_end_time = convert_time(rows[16])
        inter_start_time = convert_time(rows[19])
        inter_end_time = convert_time(rows[20])
        cus_start_time = convert_time(rows[23])
        cus_end_time = convert_time(rows[24])
        real_times = [item for item in (func_start_time, func_end_time,
                                        inter_start_time, inter_end_time,
                                        cus_start_time, cus_end_time) if item]
        tmp_max_time = max(real_times)
        tmp_min_time = min(real_times)
        max_time = tmp_max_time if tmp_max_time > max_time else max_time
        min_time = tmp_min_time if tmp_min_time < min_time else min_time

        t = Task(name, no, main_tester, support_tester,
                 func_start_time, func_end_time,
                 inter_start_time, inter_end_time,
                 cus_start_time, cus_end_time)
        all_tasks.append(t)
    print("start date from {} to {}".format(min_time, max_time))
    df = create_data_frame(all_tasks, min_time, max_time)
    df.style.apply(style_apply, colors=colors).to_excel(dst)


if __name__ == '__main__':
    main()
