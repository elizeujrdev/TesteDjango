from django.shortcuts import render
from django.http import HttpResponse
from .utilities import app_name
from .models import Actions, Notifications, Datas



context_base={'app_name':app_name}


def home(requests):
    actions=Actions.objects.all().order_by('name')
    context={'page_title':app_name, 'title': f'{app_name} | Principais Ações','actions':actions}
    context.update(context_base)
    return render(request=requests,
                  template_name='index.html',
                  context=context)


def etl(requests):
    actions=Actions.objects.all().order_by('name')
    context={'page_title': f'{app_name} | ETL','title': f'{app_name} | ETL','actions':actions}
    context.update(context_base)
    return render(request=requests,
                  template_name='etl.html',
                  context=context)


def action_detail(requests, id):
    action=Actions.objects.filter(id=id)
    datas=Datas.objects.filter(actions_id=id).order_by('-date')
    context={'page_title': f'{app_name} | ETL','title': f'{app_name} | ETL','action':action[0],'datas':datas}
    context.update(context_base)
    return render(request=requests,
                  template_name='action_detail.html',
                  context=context)




def notifications(requests):
    notifications=Notifications.objects.all()
    context={'page_title': f'{app_name} | Notificações','title': f'{app_name} | Notificações','notifications':notifications}
    context.update(context_base)
    return render(request=requests,
                  template_name='notifications.html',
                  context=context)




