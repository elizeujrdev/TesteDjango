from django.shortcuts import render
from django.http import HttpResponse
from .models import Actions, Datas
from .utilities import get_tenant
import pandas as pd



def refresh_action(requests):
    action= requests.POST.get('action')
    action_ref=Actions.objects.get(name=action)
    datas=pd.read_csv(f'https://query1.finance.yahoo.com/v7/finance/download/{action}?period1=0&period2=9999999999&interval=1d&events=history&includeAdjustedClose=true')
    for i in range(len(datas)):
        try:
            data=datas.iloc[i]
            if not Datas.objects.filter(actions_id=action_ref,date=data['Date']).exists():
                new_data=Datas(create_by=requests.user,
                               actions_id=action_ref,
                               date=data['Date'],
                               open=data['Open'],
                               high=data['High'],
                               low=data['Low'],
                               close=data['Close'],
                               adj_close=data['Adj Close'],
                               volume=data['Volume']
                               ).save()
        except Exception as e:
            return HttpResponse(f"""Errro: {e}""")


    actions=Actions.objects.all()
    context={'actions':actions}
    return render(request=requests,
                  template_name='partials/htmx_components/list_actions.html',
                  context=context)



def add_action(requests):
    action= requests.POST.get('action')
    description= requests.POST.get('description')
    if not Actions.objects.filter(name=action).exists():
        new_action=Actions(create_by=requests.user,name=action,description=description).save()
    refresh_action(requests)
    actions=Actions.objects.all()
    context={'actions':actions}
    return render(request=requests,
                  template_name='partials/htmx_components/list_actions.html',
                  context=context)




