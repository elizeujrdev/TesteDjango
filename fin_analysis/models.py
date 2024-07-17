from django.db import models
from django.contrib.auth.models import User


### Account

class Account(models.Model):
    name = models.CharField(max_length=50,blank=False,null=False,unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return f'{self.id} | {self.name}'

### TemplateBase

class TemplateBase(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.PROTECT,null=True)
    create_by = models.ForeignKey(User, on_delete=models.PROTECT,null=False)
    create_at = models.DateTimeField(auto_now=True)
    #canceled_by = models.ForeignKey(User, on_delete=models.PROTECT,null=True)
    #canceled_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['account_id','create_by','create_at']),
        ]

### Actions

class Actions(TemplateBase):
    name = models.CharField(max_length=50,blank=False,null=False,unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return f'{self.id} | {self.name}'

### Datas

class Datas(TemplateBase):
    actions_id = models.ForeignKey(Actions, on_delete=models.PROTECT,null=True)
    date=models.DateField(blank=False,null=False)
    open=models.FloatField(blank=True,null=True)
    high=models.FloatField(blank=True,null=True)
    low=models.FloatField(blank=True,null=True)
    close=models.FloatField(blank=True,null=True)
    adj_close=models.FloatField(blank=True,null=True)
    volume=models.FloatField(blank=True,null=True)

    def __str__(self) -> str:
        return f'{self.id} | {self.actions_id} | {self.date}'


class Notifications(TemplateBase):
    text = models.TextField()

    def __str__(self) -> str:
        return f'{self.id} | {self.text}'
