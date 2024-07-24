from typing import Literal
import uuid


class Component:
    def __init__(self):
        self.key=uuid.uuid4()
        self.contents=[]
        self.component_type='Component'
        self.class_css = 'generic'

    def set_class_css(self,class_css):
        self.class_css=class_css
        return self

    def add(self,content):
        if type(content) == list:
            self.contents+=content
        else:
            self.contents.append(content)
        return self

    def get_contents(self):
        return self.contents

    def clear(self):
        self.contents=[]
        return self

class Div(Component):
    def __init__(self,class_css):
        super().__init__()
        self.component_type='Div'
        self.class_css=class_css

    def render(self):
        contents_html=''
        for content in self.contents:
            contents_html+=content.render()
        return f'<div class="{self.class_css}">{contents_html}</div>'


class Page(Component):
    def __init__(self):
        super().__init__()
        self.component_type='Page'
        self.class_css='page'

    def render(self):
        contents_html=''
        for content in self.contents:
            contents_html+=f'<div class="content_page">{content.render()}</div>'
        return f'<div class="{self.class_css}">{contents_html}</div>'


class Columns(Component):
    def __init__(self):
        super().__init__()
        self.component_type='Columns'

    def render(self):
        contents_html=''
        for content in self.contents:
            contents_html+=f'<div class="col">{content.render()}</div>'
        html=f"""
    <div class="container text-center">
        <div class="row align-items-start">
        {contents_html}
        </div>
    </div>
    """
        return html


class Expander(Component):
    def __init__(self,title):
        super().__init__()
        self.component_type='Expander'
        self.title=title


    def render(self):
        contents_html=''
        for content in self.contents:
            contents_html+=content.render()

        html=f"""
    <div class="accordion accordion-flush border" id="accordionFlush{self.key}">
        <div class="accordion-item">
            <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapse{self.key}" aria-expanded="false" aria-controls="flush-collapse{self.key}">
                    {self.title}
                </button>
            </h2>
            <div id="flush-collapse{self.key}" class="accordion-collapse collapse" data-bs-parent="#accordionFlush{self.key}">
                <div class="accordion-body">
                {contents_html}
                </div>
            </div>
        </div>
    </div>
    """
        return html


class Dropdown(Component):
    def __init__(self,title,contents,type:Literal['secondary','primary']='secondary'):
        super().__init__()
        self.contents=contents
        self.component_type='Dropdown'
        self.title=title
        self.type=type

    def render(self):
        contents_html=''
        for content in self.contents:
            contents_html+=f'<li><a class="dropdown-item" href="#">{content.render()}</a></li>'
        html=f"""
        <div class="dropdown">
            <button class="btn btn-{self.type} dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                {self.title}
            </button>
            <ul class="dropdown-menu">
                {contents_html}
            </ul>
        </div>
        """
        return html


class Markdown:
    def __init__(self,content=None):
        self.component_type='Markdown'
        self.content=content

    def render(self):
        html=f'{self.content}'
        return html


class Write:
    def __init__(self,content=None):
        self.component_type='Write'
        self.content=content

    def render(self):
        html=f'{self.content.render()}'
        return html


class H:
    def __init__(self,hx,contents=''):
        self.component_type='H'
        self.contents=contents
        self.hx=hx

    def render(self):
        html=f'<p class="h{self.hx} text-center">{self.contents}</p>'
        return html


class Button:
    def __init__(self,title,action='',class_css='secondary'):
        self.component_type='Button'
        self.title=title
        self.action=action
        self.class_css=class_css

    def render(self):
        options={
            'primary':f'<button type="button" class="btn btn-primary">{self.title}</button>',
            'secondary':f'<button type="button" class="btn btn-secondary">{self.title}</button>',
            'success':f'<button type="button" class="btn btn-success">{self.title}</button>',
            'danger':f'<button type="button" class="btn btn-danger">{self.title}</button>',
            'warning':f'<button type="button" class="btn btn-warning">{self.title}</button>',
            'info':f'<button type="button" class="btn btn-info">{self.title}</button>',
            'light':f'<button type="button" class="btn btn-light">{self.title}</button>',
            'dark':f'<button type="button" class="btn btn-dark">{self.title}</button>'
            }
        return f"""<a href="{self.action}">{options[self.class_css]}</a>"""


class Table:
    def __init__(self,df,header_style:Literal['table-dark','table-light']='table-dark'):
        self.component_type='Table'
        self.df=df
        self.header_style=header_style

    def render(self):
        columns=''
        for column in self.df.columns:
            columns+=f'<th>{column}</th>'
        lines=''
        for i in range(len(self.df)):
            line_column_data=''
            for column in self.df.columns:
                dt=self.df.iloc[i][column]
                line_column_data+=f'<td>{dt}</td>'
            lines+=f'<tr>{line_column_data}</tr>'
        html=f"""
    <table class="table table-bordered" id="table_detail" style="width: 90%; margin: 0 auto; border-collapse: collapse;">
        <thead class="{self.header_style}">
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



class Card:
    def __init__(self,title,content,link=None,color_bg:Literal['bg-primary','bg-primary-subtle','bg-secondary','bg-secondary-subtle','bg-success','bg-success-subtle','bg-danger','bg-danger-subtle','bg-warning','bg-warning-subtle','bg-info','bg-info-subtle','bg-light','bg-light-subtle','bg-dark','bg-dark-subtle','bg-body-secondary','bg-body-tertiary','bg-body text-body','bg-black text-white','bg-white text-dark']='bg-body-secondary',
                 color_border:Literal['border-primary','border-primary-subtle','border-secondary','border-secondary-subtle','border-success','border-success-subtle','border-danger','border-danger-subtle','border-warning','border-warning-subtle','border-info','border-info-subtle','border-light','border-light-subtle','border-dark','border-dark-subtle','border-black','border-white']='border-success'):
        self.component_type='Table'
        self.title=title
        self.content=content
        self.link=link
        self.color_bg=color_bg
        self.color_border=color_border
        
    def render(self): 
        if self.link == None:
            self.link=''
        else:
            self.link=f'href="{self.link}"'
        html=f"""
    <div class="container border-start border-5 {self.color_border} p-3 mb-2 {self.color_bg} rounded">
        <a {self.link} style="text-decoration: none; color: inherit; ">
            <h5 class="card-title">
                {self.title}
            </h5>
        </a>
        <p class="card-text">
            {self.content}
        </p>
    </div>
    """
        return html

class ButtonV2:
    def __init__(self,title,action='',class_css='btn btn-outline-danger'):
        self.component_type='ButtonV2'
        self.title=title
        self.action=action
        self.class_css=class_css

    def render(self):
        html=f"""<a href="{self.action}"><button type="button" class="{self.class_css}" id="{self.title}">Botão</button></a>"""
        return html




class Toggle:
    def __init__(self,title):
        self.component_type='Toggle'
        self.title=title

    def render(self):
        html=f"""<p><div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault">
                    <label class="form-check-label" for="flexSwitchCheckDefault">{self.title}</label>
                  </div>"""
        return html