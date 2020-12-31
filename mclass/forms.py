'''
Created on 2020年12月14日

@author: Administrator
'''
from django import forms

class MclassForm(forms.Form):
    id = forms.IntegerField(required=False, )
    mtype = forms.CharField(label='材料类别', max_length=128, strip=True, widget=forms.TextInput(attrs={'id':'mtype', 'class': 'form-control', 'style':"width:150px", 'value':''}))
    mclass = forms.CharField(label='材料小类', max_length=128, strip=True, widget=forms.TextInput(attrs={'id':'mclass', 'class': 'form-control', 'style':"width:150px", 'value':''}))
    content = forms.CharField(required=False, label='核算内容', max_length=256, widget=forms.Textarea(attrs={'id':'content', 'class': 'form-control', 'style':"height:100px", 'value':''}))
    remark = forms.CharField(required=False, label='备注', max_length=256, widget=forms.Textarea(attrs={'id':'remark', 'class': 'form-control', 'style':"height:100px", 'value':''}))