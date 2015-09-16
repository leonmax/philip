# -*- coding: utf-8 -*-

from prettytable import PrettyTable


def dict_to_table(d, keys, sort=None):
    table = PrettyTable(field_names=sorted(keys), sortby=sort)
    table.padding_width = 1
    for i in d:
        table.add_row([i[x] for x in sorted(i.keys()) if x in keys])
    print(table)


