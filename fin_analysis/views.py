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
from testdjango.components import components as cmp



context_base={'app_name':app_name,'notifications_counts':0}


def refresh_context_base(requests):
    context_aux={}
    context_aux['notifications_counts']=Notifications.objects.filter(create_by=requests.user).count()
    return context_aux


def home(requests):
    actions=Actions.objects.all().order_by('description')
    context={'page_title':app_name, 'title': f'{app_name} | Principais Ações','actions':actions}
    context.update(refresh_context_base(requests))
    return render(request=requests,
                  template_name='index.html',
                  context=context)

def drafts(requests):
    context={'page_title':f'{app_name} | Drafts', 'title': f'{app_name} | Drafts'}
    context.update(refresh_context_base(requests))
    content_view=''

    
    content_view+=cmp.h(f"Titulo H1",1)
    content_view+=cmp.columns([cmp.h('Coluna 1',2),cmp.h('Coluna 2',2),cmp.h('Coluna 3',2),cmp.h('Coluna 4',2),cmp.h('Coluna 5',2)])

    content_view+=cmp.columns([cmp.card('Card 1','Conteúdo XYZ 1','/'),cmp.card('Card 2','Conteúdo XYZ 2',color_bg='bg-danger-subtle'),cmp.card('Card 3','Conteúdo XYZ 3',color_border='border-dark')])

    content_view+=cmp.buttom('Botao Link /etl/','/etl/')
    content_view+=cmp.dropdown('Dropdown',['Item 1','Item 2',cmp.buttom('Item 3 Botao Link /etl/','/etl/')],'primary')
    content_view+=cmp.expander('Expander 1','<p>Conteúdo Expander 1</p>','exp_1')
    content_view+=cmp.expander('Expander 2','<p>Conteúdo Expander 2</p>','exp_2')
    content_view+=cmp.expander('Expander com componente Tabela',cmp.table(pd.DataFrame(list(Actions.objects.all().values()))),'exp_tb')

    


    context.update({'content_view':content_view})
    return render(request=requests,
                  template_name='drafts.html',
                  context=context)




def etl(requests):
    actions=Actions.objects.all().order_by('description')
    context={'page_title': f'{app_name} | ETL','title': f'{app_name} | ETL','actions':actions}
    context.update(refresh_context_base(requests))
    return render(request=requests,
                  template_name='etl.html',
                  context=context)



def action_detail(requests, id):
    content_view=''
    action=Actions.objects.get(id=id)

    #cache = CachePickle(expiration=60*5)
    #cached_value = cache.get(action.name)
    #if cached_value:
    #    datas=cached_value
    #else:
    #    datas = Datas.objects.filter(actions_id=id)
    #    cache.set(action.name, datas)

    datas = Datas.objects.filter(actions_id=id)

    context={'page_title': f'{app_name} | ETL','title': f'{app_name} | ETL','action':action,'action_title':f'{action.id} | {action.name} | {action.description}'}
    try:
        df = pd.DataFrame(list(datas.values()))
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
        ultima_linha=df.iloc[len(df)-1]
        content_view+=cmp.columns([cmp.card(f'Qtde.',len(df)),
                                   cmp.card(f'Date',ultima_linha['date']),
                                   cmp.card(f'Open',ultima_linha['open']),
                                   cmp.card(f'High',ultima_linha['high']),
                                   cmp.card(f'Low',ultima_linha['low']),
                                   cmp.card(f'Close',ultima_linha['close']),
                                   cmp.card(f'Adj Close',ultima_linha['adj_close'])
                                   ])
        content_view+=graph_html
        content_view+=cmp.expander('Detail',cmp.table(df),key='exp_tb_detail')
        context.update({'content_view':content_view})
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




