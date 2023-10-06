from django.shortcuts import render
from django.http import FileResponse
from .models import Robot
import pandas as pd
import datetime


def get_serial(model: str, version: str) -> str:
    bar = "-"
    serial = model + bar + version
    return serial


def get_data():
    week_number = datetime.datetime.today().isocalendar()[1]
    info = Robot.objects.all()
    res = {}
    count = 0
    for elem in info:
        if elem.created.isocalendar()[1] == week_number:
            if elem.serial in res.keys():
                res[elem.serial] += 1
            else:
                res[elem.serial] = 1
            count += 1
    return res


def convertation():
    dt = {}
    result = []
    data = get_data()
    for k, v in data.items():
        model = k.split('-')[0]
        series = k.split('-')[1]
        if model not in dt.keys():
            dt[model] = [[series], [v]]
        else:
            val = dt[model]
            val[0].append(series)
            val[1].append(v)

    for k, v in dt.items():
        res = {'Модель': [],
               'Версия': [],
               'Количество за неделю': v[1]}
        for ser in v[0]:
            res['Модель'].append(k)
            res['Версия'].append(ser)
        result.append(res)
    return result


def create_excel():
    dataframes = convertation()
    with pd.ExcelWriter('R4C/static/results_per_week.xlsx') as writer:
        for elem in dataframes:
            res = pd.DataFrame(elem).sort_values(by='Количество за неделю',
                                                 ascending=False)
            res.index = ['->' for _ in range(len(elem['Модель']))]
            name = elem['Модель'][0]
            res.to_excel(writer, sheet_name=name)


# Create your views here.
def index(request):
    return render(request, 'index.html')


def send_excel(request):
    try:
        create_excel()
    except IndexError:
        errors = {'error': 'Данные о роботах еще не внесены.'}
        return render(request, 'index.html', {'errors': errors})
    response = FileResponse(open('R4C/static/results_per_week.xlsx', 'rb'))
    return response
