import csv
import os
import datetime
from collections import defaultdict
from copy import deepcopy
from itertools import combinations


# 1. Open file and read it
# This folder contains csv files
path = '.\\files\\'
files_csv = os.listdir(path)
informaion = defaultdict(list)
short_informaion = []
dates = set()
counter = 0
for f in files_csv:
    with open(path + f) as File:
        reader = csv.reader(File)
        for row in reader:
            try:
                date_time = datetime.datetime(*map(int, [
                    row[0][:4],
                    row[0][4:6],
                    row[0][6:],
                    row[1][:2],
                    row[1][2:4]
                    ]
                    )
                )
                if date_time.date() not in dates:
                    short_informaion.append(
                        (
                            date_time.date(),
                            float(row[2]),
                            counter
                        )
                    )
                    counter += 1
                    dates.add(date_time.date())
                informaion[date_time.date()].append(
                    (
                        date_time,
                        float(row[2])
                    )
                )
            except ValueError:
                continue
print('CSV file store information of', len(informaion), 'days')


# Function of calculation profit
def calc_profit(transactions):
    return sum(t['sell'][1] - t['buy'][1] for t in transactions)


# Find one most expensive in list of short information
def find_one_most_expensive(info):
    info = deepcopy(info)
    lenght = len(info)
    info.sort(key=lambda x: x[1])
    result = {'buy': None, 'sell': None}
    max_cost = 0
    for i in range(lenght//2):
        for j in range(lenght - 1, lenght // 2, -1):
            if (info[j][1] - info[i][1] > max_cost
                and info[j][0] - info[i][0] > datetime.timedelta()):
                max_cost = info[j][1] - info[i][1]
                result['buy'], result['sell'] = info[i], info[j]
    return result


# First taсtic
def first_taсtics(info, short_info):
    short_find = find_one_most_expensive(short_info)
    result = []
    if short_find['buy'] is not None or short_find['sell'] is not None:
        day_buy = short_find['buy'][0]
        day_sell = short_find['sell'][0]
        result.append(find_one_most_expensive(info[day_buy] + info[day_sell]))
        result[0]['buy'] += (short_find['buy'][2],)
        result[0]['sell'] += (short_find['sell'][2],)
    return result


# Print information of selected transaction
def information_of_transaction(transactions):
    overal_income = calc_profit(transactions)
    for i, t in enumerate(transactions, 1):
        print(
            f'{i}. Акция куплена ', t['buy'][0], 'за:', t['buy'][1],
            '; Продана', t['sell'][0], 'за:', t['sell'][1],
            '; Прибыль:', t['sell'][1] - t['buy'][1]
            )
    print('\tОбщая прибыль:', overal_income)


# Find split one long transaction to two for more profit
def split_span(short_info, start, end):
    max_cost = short_info[end][1] - short_info[start][1]
    info = [x[1] for x in short_info]
    index = None
    for i in range(start+10, end-10):
        l1 = info[start:i]
        l2 = info[i:end+1]
        price = max(l1) - min(l1) + max(l2) - min(l2)
        if price - 50 > max_cost:
            max_cost = price
            index = start, i-1, i, end
    return index


# Second taсtic
def second_taсtics(info, short_info):
    lenght = len(short_info)
    one_long_trans = first_taсtics(info, short_info)
    start = one_long_trans[0]['buy'][2]
    end = one_long_trans[0]['sell'][2]
    other = []
    if start > 10:
        other.extend(first_taсtics(info, short_info[:start]))
    if end < lenght - 10:
        other.extend(first_taсtics(info, short_info[end:]))
    tactics = list(zip(one_long_trans * len(other), other))
    tactics.append(one_long_trans)
    index = split_span(short_info, start, end)
    if index is not None:
        tactics.extend([
            first_taсtics(info, short_info[index[0]: index[1]]),
            first_taсtics(info, short_info[index[2]: index[3]])])
    max_cost = 0
    strategy = None
    for x in tactics:
        income = calc_profit(x)
        if max_cost < income:
            max_cost = income
            strategy = x
    return sort_taсtics(strategy)


def sort_taсtics(taсtics):
    taсtics = list(taсtics)
    taсtics.sort(key=lambda x: x['buy'][2])
    return taсtics


def check(indexes):
    indexes = list(indexes)
    lenght = len(indexes)
    indexes.sort(key=lambda x: x[0])
    starts = [_[0] for _ in indexes]
    ends = [_[1] for _ in indexes]
    if lenght != len(set(starts)) and lenght != len(set(ends)):
        return False
    if any([i for i in range(lenght - 1) if starts[i+1] - ends[i] < 0]):
        return False
    return True




def third_taсtics(info, short_info, *, k=1):
    lenght = len(short_info)
    one_long_trans = first_taсtics(info, short_info)
    start = one_long_trans[0]['buy'][2]
    end = one_long_trans[0]['sell'][2]
    indexes = [(start, end)]
    if start > 10:
        indexes.append((0, start))
    if end < lenght - 10:
        indexes.append((end, lenght-1))
    i = 0
    while len(indexes) < k + 4:
        ind = split_span(short_info, *indexes[i])
        if ind is not None:
            indexes.extend([(ind[0], ind[1]), (ind[2], ind[3])])
        i += 1
        if i == len(indexes):
            break
    max_cost = 0
    best_taсtics = None
    if len(indexes) < k:
        k = len(indexes)
    for i in range(k, 2, -1):
        for _, taсtics in enumerate(combinations(indexes, i)):
            cost = []
            if check(taсtics):
                for ind in taсtics:
                    cost.extend(first_taсtics(info, short_info[ind[0]: ind[1]]))
                profit = calc_profit(cost)
                if profit > max_cost:
                    max_cost = profit
                    best_taсtics = cost
            else:
                continue
    return sort_taсtics(best_taсtics)


# information_of_transaction(first_taсtics(informaion, short_informaion))
# information_of_transaction(second_taсtics(informaion, short_informaion))
# information_of_transaction(third_taсtics(informaion, short_informaion, k=4))

print('\tInput type of transactions:\n1\tOne transaction\n2\tTwo transaction\
\n3\tK transactions')
while True:
    try:
        print('>>>', end='   ')
        type = int(input())
        if type in {1, 2, 3}:
            break
        raise ValueError
    except ValueError:
        print('Type again')

if type == 3:
    print('\tInput K')
    while True:
        try:
            print('>>>', end='   ')
            K = int(input())
            if K > 0:
                break
            raise ValueError
        except ValueError:
            print('Type again')

if type == 1:
    information_of_transaction(first_taсtics(informaion, short_informaion))
elif type == 2:
    information_of_transaction(second_taсtics(informaion, short_informaion))
elif type == 3:
    information_of_transaction(third_taсtics(informaion, short_informaion, k=K))
