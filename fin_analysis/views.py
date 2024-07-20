from django.shortcuts import render
from django.http import HttpResponse
from .utilities import app_name
from .models import Actions, Notifications, Datas
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .utilities import CachePickle
import plotly.express as px
from django.shortcuts import render
import pandas as pd


context_base={'app_name':app_name,'notifications_counts':0}


def refresh_context_base(requests):
    context_aux={}
    context_aux['notifications_counts']=Notifications.objects.filter(create_by=requests.user).count()
    return context_aux


def home(requests):
    actions=Actions.objects.all().order_by('name')
    context={'page_title':app_name, 'title': f'{app_name} | Principais Ações','actions':actions}
    context.update(refresh_context_base(requests))
    return render(request=requests,
                  template_name='index.html',
                  context=context)


def etl(requests):
    actions=Actions.objects.all().order_by('name')
    context={'page_title': f'{app_name} | ETL','title': f'{app_name} | ETL','actions':actions}
    context.update(refresh_context_base(requests))
    return render(request=requests,
                  template_name='etl.html',
                  context=context)



def action_detail(requests, id):
    action=Actions.objects.get(id=id)
    cache = CachePickle(expiration=60*5)
    cached_value = cache.get(action.name)
    if cached_value:
        datas=cached_value
    else:
        datas = Datas.objects.filter(actions_id=id)
        cache.set(action.name, datas)

    context={'page_title': f'{app_name} | ETL','title': f'{app_name} | ETL','action':action,'action_title':f'{action.id} | {action.name} | {action.description}','datas':datas}

    try:
        df = pd.DataFrame(list(datas.values()))
        print(df.columns)
        fig = px.line(df,x='date',y=['open','high','low','close','adj_close'])


        fig.update_layout(
            plot_bgcolor='#FAFAFA',  # Cor de fundo do gráfico
            paper_bgcolor='white',  # Cor de fundo da área do gráfico
            legend=dict(
                title=dict(text='Indicadores', font=dict(size=16, color='black')),
                x=0.5,  # Posiciona a legenda horizontalmente dentro do gráfico
                y=0.1,  # Posiciona a legenda verticalmente dentro do gráfico
                xanchor='center',  # Alinha horizontalmente ao centro
                yanchor='bottom',  # Alinha verticalmente ao fundo
                orientation='h',  # Orientação horizontal
                bgcolor='rgba(255, 255, 255, 0.8)'  # Cor de fundo da legenda com transparência
            ),
            xaxis_title=None,
            yaxis_title=None,
            xaxis=dict(
                title_font=dict(size=18, color='black'),
                tickfont=dict(size=14, color='black')
            ),
            yaxis=dict(
                title_font=dict(size=18, color='black'),
                tickfont=dict(size=14, color='black')
            ),
            annotations=[
                dict(
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=0.9,
                    text='Timeline',
                    showarrow=False,
                    font=dict(size=24, color='black'),
                    align='center'
                )
            ]
        )
        graph_html = fig.to_html(full_html=False)
        context.update({'graph_html':graph_html})
    except:
        pass



    context.update(refresh_context_base(requests))
    return render(request=requests,
                  template_name='action_detail.html',
                  context=context)




def notifications(requests):
    notifications=Notifications.objects.all()
    context={'page_title': f'{app_name} | Notificações','title': f'{app_name} | Notificações','notifications':notifications}
    context.update(refresh_context_base(requests))
    return render(request=requests,
                  template_name='notifications.html',
                  context=context)




