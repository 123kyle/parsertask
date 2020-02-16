#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime, timedelta


class Task:

    def __init__(self, name, no, main_tester,
                 support_tester,
                 func_start_time, func_end_time,
                 inter_start_time, inter_end_time,
                 cus_start_time, cus_end_time):
        self.name = name
        self.no = no
        self.main_tester = main_tester
        self.support_tester = support_tester
        self.func_start_time = func_start_time
        self.func_end_time = func_end_time
        self.inter_start_time = inter_start_time
        self.inter_end_time = inter_end_time
        self.cus_start_time = cus_start_time
        self.cus_end_time = cus_end_time

    def to_list(self, start, end):
        if not isinstance(start, datetime) or not isinstance(end, datetime):
            return

        data = [self.main_tester, self.support_tester,
                self.name, self.no]
        current_day = start
        step = timedelta(days=1)
        while current_day <= end:
            if current_day.weekday() >= 5:
                data.append(10)
            else:
                if (self.func_start_time and self.func_end_time and
                        current_day >= self.func_start_time and current_day <= self.func_end_time):
                    data.append(1)

                elif (self.inter_start_time and self.inter_end_time and
                      current_day >= self.inter_start_time and current_day <= self.inter_end_time):
                    data.append(2)
                elif (self.cus_start_time and self.cus_end_time and
                      current_day >= self.cus_start_time and current_day <= self.cus_end_time):
                    data.append(3)
                else:
                    data.append(0)
            current_day += step
        return data
