'''
Created on 2020年12月22日

@author: wqx
'''
from django import forms

from mclass.models import Mclass
from project.models import Project


class InStoreForm(forms.Form):
    id = forms.IntegerField(required=False, )
    date = forms.DateField(label='入库日期', widget=forms.DateInput(attrs={'id': 'date', 'type': 'date', 'class': 'form-control', 'style': "width:180px",}))
    receiptNo = forms.CharField(label='入库单号', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'receiptNo', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    mtype = forms.CharField(label='材料分类', max_length=128, strip=True, widget=forms.Select(attrs={'id': 'mtype', 'class': 'form-control', 'style': "width:180px", 'value': ''}, choices=Mclass().getMtypeDropDownList()))
    mclass = forms.CharField(label='材料小类', max_length=128, strip=True, widget=forms.Select(attrs={'id': 'mclass', 'class': 'form-control', 'style': "width:180px", 'value': ''}, choices=Mclass().getMclassDropDownList()))
    mname = forms.CharField(label='材料名称', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'mname', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    specifi = forms.CharField(label='品牌/规格/型号', max_length=128, strip=True, widget=forms.TextInput(attrs={'id':'specifi', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    num = forms.CharField(label='数量', max_length=16, strip=True, widget=forms.TextInput(attrs={'id': 'num', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    unit = forms.CharField(label='单位', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'unit', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    factory = forms.CharField(required=False, label='厂家名称', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'factory', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    materialfee = forms.CharField(label='材料费', max_length=128, strip=True, widget=forms.TextInput(attrs={'id':'materialfee', 'type': 'number', 'min': "0", 'class': 'form-control', 'style':"width:180px", 'value': ''}))
    price = forms.CharField(label='税后单价', max_length=10, strip=True, widget=forms.TextInput(attrs={'id': 'price', 'type': 'number', 'min': "0", 'class': 'form-control', 'style': "width:180px", 'value': '', 'readonly': 'true'}))
    rate = forms.CharField(required=False, label='税率', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'rate', 'type': 'number', 'min': "0", 'max': "1", 'step': "0.01", 'class': 'form-control', 'style':"width:180px", 'value': ''}))
    buyer = forms.CharField(label='采购人', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'buyer', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    inspector = forms.CharField(label='验收员', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'inspector', 'class': 'form-control', 'style':"width:180px", 'value': ''}))
    storeloc = forms.CharField(required=False, label='仓库', max_length=128, widget=forms.TextInput(attrs={'id': 'storeloc', 'class': 'form-control', 'style':"width:180px", 'value': ''}))
    project = forms.CharField(label='所属项目', max_length=128, strip=True, widget=forms.Select(attrs={'id': 'project', 'class': 'form-control', 'style': "width:180px", 'value': ''}, choices=Project().getProjectDropDownList()))
    provider = forms.CharField(label='供货单位', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'provider', 'class': 'form-control', 'style':"width:180px", 'value':''}))
    remark = forms.CharField(required=False, label='备注', max_length=256, widget=forms.Textarea(attrs={'id': 'remark', 'class': 'form-control', 'style':"width:180px; height:60px", 'value':''}))


class OutStoreForm(forms.Form):
    id = forms.IntegerField(required=False, )
    date = forms.DateField(label='出库日期', widget=forms.DateInput(attrs={'id': 'date', 'type': 'date', 'class': 'form-control', 'style': "width:180px"}))
    outNo = forms.CharField(label='出库单号', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'outNo', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    toWhere = forms.CharField(label='工程部位', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'toWhere', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    mtype = forms.CharField(required=False, label='材料分类', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'mtype', 'class': 'form-control', 'style': "width:180px", 'value': '', 'readonly': 'true'}))
    mclass = forms.CharField(required=False, label='材料小类', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'mclass', 'class': 'form-control', 'style': "width:180px", 'value': '', 'readonly': 'true'}))
    mname = forms.CharField(required=False, label='材料名称', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'mname', 'class': 'form-control', 'style': "width:180px", 'value': '', 'readonly': 'true'}))
    specifi = forms.CharField(required=False, label='品牌/规格/型号', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'specifi', 'class': 'form-control', 'style': "width:180px", 'value': '', 'readonly': 'true'}))
    num = forms.CharField(label='出库数量', max_length=16, strip=True, widget=forms.TextInput(attrs={'id':'num', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    demount = forms.CharField(required=False, label='扣款金额', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'demount', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    unit = forms.CharField(required=False, label='单位', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'unit', 'class': 'form-control', 'style': "width:180px", 'value': '', 'readonly': 'true'}))
    reciTeam = forms.CharField(label='自用/班组', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'reciTeam', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    receiver = forms.CharField(label='领用人', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'receiver', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    store = forms.CharField(label='库存id', max_length=128, strip=True, widget=forms.TextInput(attrs={'id':'store', 'class': 'form-control', 'style': "width:180px", 'value': ''}))
    pname = forms.CharField(required=False, label='所属项目', max_length=128, strip=True, widget=forms.TextInput(attrs={'id': 'pname', 'class': 'form-control', 'style': "width:180px", 'value': '', 'readonly': 'true'}))
    remark = forms.CharField(required=False, label='备注', max_length=256, widget=forms.Textarea(attrs={'id': 'remark', 'class': 'form-control', 'style': "width:180px; height:60px", 'value': ''}))
