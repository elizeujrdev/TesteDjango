from typing import Literal




def columns(columns):
    html_columns=''
    for column in columns:
        html_columns+=f'<div class="col">{column}</div>'
    html=f"""
<div class="container text-center">
    <div class="row align-items-start">
    {html_columns}
    </div>
</div>
"""
    return html


def h(content,hx):
    html=f'<p class="h{hx} text-center">{content}</p>'
    return html


def buttom(title,action='',type='secondary'):
    options={
        'primary':f'<button type="button" class="btn btn-primary">{title}</button>',
        'secondary':f'<button type="button" class="btn btn-secondary">{title}</button>',
        'success':f'<button type="button" class="btn btn-success">{title}</button>',
        'danger':f'<button type="button" class="btn btn-danger">{title}</button>',
        'warning':f'<button type="button" class="btn btn-warning">{title}</button>',
        'info':f'<button type="button" class="btn btn-info">{title}</button>',
        'light':f'<button type="button" class="btn btn-light">{title}</button>',
        'dark':f'<button type="button" class="btn btn-dark">{title}</button>'
        }
    return f"""<a href="{action}">{options[type]}</a>"""


def expander(title,body,key):
    html=f"""
<div class="accordion accordion-flush border" id="accordionFlush{key}">
    <div class="accordion-item">
        <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapse{key}" aria-expanded="false" aria-controls="flush-collapse{key}">
                {title}
            </button>
        </h2>
        <div id="flush-collapse{key}" class="accordion-collapse collapse" data-bs-parent="#accordionFlush{key}">
            <div class="accordion-body">
            {body}
            </div>
        </div>
    </div>
</div>
"""
    return html




def dropdown(title,itens,type:Literal['secondary','primary']='secondary'):
   list_itens=''
   for item in itens:
       list_itens+=f'<li><a class="dropdown-item" href="#">{item}</a></li>'
   html=f"""
<div class="dropdown">
    <button class="btn btn-{type} dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
        {title}
    </button>
    <ul class="dropdown-menu">
        {list_itens}
    </ul>
</div>
"""
   return html



def card(title,content,link=None,color_bg:Literal['bg-primary','bg-primary-subtle','bg-secondary','bg-secondary-subtle','bg-success','bg-success-subtle','bg-danger','bg-danger-subtle','bg-warning','bg-warning-subtle','bg-info','bg-info-subtle','bg-light','bg-light-subtle','bg-dark','bg-dark-subtle','bg-body-secondary','bg-body-tertiary','bg-body text-body','bg-black text-white','bg-white text-dark']='bg-body-secondary',
         color_border:Literal['border-primary','border-primary-subtle','border-secondary','border-secondary-subtle','border-success','border-success-subtle','border-danger','border-danger-subtle','border-warning','border-warning-subtle','border-info','border-info-subtle','border-light','border-light-subtle','border-dark','border-dark-subtle','border-black','border-white']='border-success'):
    if link == None:
        link=''
    else:
        link=f'href="{link}"'
    html=f"""
<div class="container border-start border-5 {color_border} p-3 mb-2 {color_bg} rounded">
    <a {link} style="text-decoration: none; color: inherit; ">
        <h5 class="card-title">
            {title}
        </h5>
    </a>
    <p class="card-text">
        {content}
    </p>
</div>
"""
    return html



def table(df,header_style:Literal['table-dark','table-light']='table-dark' ):
    columns=''
    for column in df.columns:
        columns+=f'<th>{column}</th>'
    lines=''
    for i in range(len(df)):
        line_column_data=''
        for column in df.columns:
            dt=df.iloc[i][column]
            line_column_data+=f'<td>{dt}</td>'
        lines+=f'<tr>{line_column_data}</tr>'
    html=f"""
<table class="table table-hover" id="table_detail" style="width: 90%; margin: 0 auto; border-collapse: collapse;">
    <thead class="{header_style}">
        <tr>
        {columns}
        </tr>
    </thead>
    <tbody>
        {lines}
    </tbody>
</table>
"""
    return html






