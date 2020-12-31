'''
Created on 2020年12月14日

@author: Administrator
'''
from django import forms

class ProjectForm(forms.Form):
    id = forms.IntegerField(required=False, )
    code = forms.CharField(label='项目编号', max_length=128, strip=True, widget=forms.TextInput(attrs={'id':'code', 'class': 'form-control', 'style':"width:150px", 'value':''}))
    name = forms.CharField(label='项目名称', max_length=128, strip=True, widget=forms.TextInput(attrs={'id':'name', 'class': 'form-control', 'style':"width:150px", 'value':''}))
    remark = forms.CharField(required=False, label='备注', max_length=256, widget=forms.Textarea(attrs={'id':'remark', 'class': 'form-control', 'style':"height:150px", 'value':''}))