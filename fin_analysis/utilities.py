app_name='FinancePro'



def get_tenant(requests):
    return requests.get_host().split('.')[0]


def get_path(requests):
    path=requests.build_absolute_uri().split('/')
    if len(path)<=4:
        return 'HOME'
    else:
        return path[-2].upper()
