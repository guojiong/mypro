from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from HTMLTable import HTMLTable
from mclass.models import Mclass
from store.models import OutStore, InStore


def totals_report(request):
    flag = request.POST.get('csrfmiddlewaretoken')
    if flag:
        project = request.POST.get('project')
        year_month = request.POST.get('year_month')

        # 报表标题
        title = '重庆明珠建设（集团）有限公司 %s 月材料报表' % year_month
        table_head = HTMLTable(caption=title)
        table_head.append_data_rows((
            ('单位：', project, '', '', '', '', '', '', '', '单位：', '元'),
        ))
        # 报表头
        # 标题样式
        table_head.caption.set_style({
            'text-align': 'center',
            'font-size': '30px',
        })

        # 表格样式，即<table>标签样式
        table_head.set_style({
            'margin': "0 auto",
            'border-collapse': 'collapse',
            'word-break': 'keep-all',
            'white-space': 'nowrap',
            'font-size': '14px',
        })
        # 统一设置所有单元格样式，<td>或<th>
        table_head.set_cell_style({
            'text-align': 'center',
            'border-color': '#000',
            'border-width': '0px',
            'border-style': 'solid',
            'padding': '8px',
            'min-width': '50px'
        })
        # 字体调整
        table_head[0].set_cell_style({
            'font-weight': '800',
            'border-style': 'solid',
            'padding': '8px',
            'font-size': '15px',
        })

        # 报表主体
        # 标题
        table_body = HTMLTable()

        # 表头行
        table_body.append_header_rows((
            ('序号', '材料分类', '', '', '上期结存金额', '入库金额', '', '出库金额', '', '本期结存金额', '备注'),
            ('', '', '', '', '', '本期', '累计', '本期', '累计', '', ''),
        ))

        # 合并单元格
        table_body[0][0].attr.rowspan = 2
        table_body[0][1].attr.rowspan = 2
        table_body[0][1].attr.colspan = 3
        table_body[0][4].attr.rowspan = 2
        table_body[0][5].attr.colspan = 2
        table_body[0][7].attr.colspan = 2
        table_body[0][7].attr.colspan = 2
        table_body[0][9].attr.rowspan = 2
        table_body[0][10].attr.rowspan = 2

        list_data = []
        mtype_num = Mclass.objects.values('mtype').annotate(c=Count('mclass')).values('mtype', 'c')
        m_data = Mclass.objects.values('mtype', 'mclass').all()
        # main_data = Store.objects.annotate(np=F('num') * F('price')).values('mtype', 'mclass', 'num', 'price')
        # .aggregate(all_cost=Sum(F("num") * F("price"), output_field=models.FloatField()))
        m1 = ['主要材料', '结构件', '其他材料']
        format_table = {}
        report_order = 1
        for num in mtype_num:
            format_table[num['mtype']] = num['c']
            if num['mtype'] in m1:
                is_first = True
                for m in m_data:
                    if m['mtype'] == num['mtype']:
                        if is_first and report_order == 1:
                            list_data.append((report_order, '材料', m['mtype'], m['mclass'], '', '', '', '', '', '', ''))
                            is_first = False
                        elif is_first:
                            list_data.append((report_order, '', m['mtype'], m['mclass'], '', '', '', '', '', '', ''))
                            is_first = False
                        else:
                            list_data.append((report_order, '', '', m['mclass'], '', '', '', '', '', '', ''))
                        report_order = report_order + 1

        for row in table_body.iter_data_rows():
            if row[1].value == '材料':
                row[1].attr.rowspan = report_order  # 设置材料跨行数
        list_data.append((report_order, '', '材料小计', '', '', '', '', '', '', '', ''))
        report_order = report_order + 1
        list_data.append((report_order, '（方）辅助材料', '', '', '', '', '', '', '', '', ''))
        report_order = report_order + 1
        for num in mtype_num:
            if num['mtype'] not in m1:
                is_first = True
                for m in m_data:
                    if m['mtype'] == num['mtype']:
                        if is_first and report_order == 1:
                            list_data.append((report_order, '材料', m['mtype'], m['mclass'], '', '', '', '', '', '', ''))
                            is_first = False
                        elif is_first:
                            list_data.append((report_order, m['mtype'], '', m['mclass'], '', '', '', '', '', '', ''))
                            is_first = False
                        else:
                            list_data.append((report_order, '', '', m['mclass'], '', '', '', '', '', '', ''))
                        report_order = report_order + 1
                list_data.append((report_order, '', '', '小计', '', '', '', '', '', '', ''))
                report_order = report_order + 1
        list_data.append(('合计', '', '', '', '', '', '', '', '', '', ''))

        # 数据行
        table_body.append_data_rows(list_data)

        # 表格样式，即<table>标签样式
        table_body.set_style({
            'margin': "0 auto",
            'border-collapse': 'collapse',
            'word-break': 'keep-all',
            'white-space': 'nowrap',
            'font-size': '14px',
        })

        # 统一设置所有单元格样式，<td>或<th>
        table_body.set_cell_style({
            'text-align': 'center',
            'border-color': '#000',
            'border-width': '1px',
            'border-style': 'solid',
            'padding': '5px',
            'width': '50px',
        })

        # 表头样式
        table_body.set_header_row_style({
            'color': '#fff',
            # 'background-color': '#48a6fb',
            'background-color': '#4682B4',
            'font-size': '18px',
        })

        # 覆盖表头单元格字体样式
        table_body.set_header_cell_style({
            'padding': '15px',
        })

        # 调小次表头字体大小
        table_body[1].set_cell_style({
            'padding': '8px',
            'font-size': '15px',
        })

        # 遍历数据行，如果增长量为负，标红背景颜色
        for row in table_body.iter_data_rows():
            if row[2].value == '材料小计':
                row[2].attr.colspan = 2
            for g in format_table.keys():
                if row[2].value in m1 and row[2].value == g:
                    row[2].attr.rowspan = format_table[g]
            for g in format_table.keys():
                if row[1].value is not '' and row[1].value not in m1 and row[1].value == g:
                    row[1].attr.rowspan = format_table[g] + 1
                    row[1].attr.colspan = 2
            if row[1].value == '（方）辅助材料':
                row[1].attr.colspan = 3
            if row[1].value == '材料':
                row[1].attr.rowspan = 13
            if row[0].value == '合计':
                row[0].attr.colspan = 4

            row.set_style({
                'background-color': 'white',
                'word-break': 'break-all',
                'word-wrap': 'break-word'
            })

        # 报表表脚
        table_footer = HTMLTable()
        table_footer.append_data_rows((
            ('负责人：', '测试人', '', '', '', '物资部：', '测试人', '', '', '制表人：', '测试人'),
        ))
        # 表格样式，即<table>标签样式
        table_footer.set_style({
            'margin': "0 auto",
            'border-collapse': 'collapse',
            'word-break': 'keep-all',
            'white-space': 'nowrap',
            'font-size': '14px',
        })
        # 统一设置所有单元格样式，<td>或<th>
        table_footer.set_cell_style({
            'text-align': 'center',
            'border-color': '#000',
            'border-width': '0px',
            'border-style': 'solid',
            'padding': '8px',
            'min-width': '80px'
        })
        # 字体调整
        table_footer[0].set_cell_style({
            'font-weight': '800',
            'border-style': 'solid',
            'padding': '8px',
            'font-size': '15px',
        })

        html = table_head.to_html() + table_body.to_html() + table_footer.to_html()
        return JsonResponse({'Content': html}, safe=False)
    return render(request, 'reports/totals.html')


def team_details_report(request):
    flag = request.POST.get('csrfmiddlewaretoken')
    if flag:
        project_name = request.POST.get('project')
        team_name = request.POST.get('team')

        # 报表标题
        title = '班组领用明细'
        table_head = HTMLTable(caption=title)
        table_head.append_data_rows((
            ('', '项目名称：', project_name, '', '', '', '', '', '', '', '', '', '班组名称：', team_name, '',),
        ))
        # 报表头
        # 标题样式
        table_head.caption.set_style({
            'text-align': 'center',
            'font-size': '30px',
        })

        # 表格样式，即<table>标签样式
        table_head.set_style({
            'margin': "0 auto",
            'border-collapse': 'collapse',
            'word-break': 'keep-all',
            'white-space': 'nowrap',
            'font-size': '15px',
        })
        # 统一设置所有单元格样式，<td>或<th>
        table_head.set_cell_style({
            'text-align': 'center',
            'border-color': '#000',
            'border-width': '0px',
            'border-style': 'solid',
            'padding': '8px',
            'min-width': '80px'
        })
        # 字体调整
        table_head[0].set_cell_style({
            'font-weight': '800',
            'border-style': 'solid',
            'padding': '8px',
            'font-size': '15px',
        })

        # 报表主体
        # 标题
        table_body = HTMLTable()

        # 表头行
        table_body.append_header_rows((
            ('日期', '单据编号', '材料类别', '材料小类', '材料名称', '品牌/规格/型号', '厂家名称', '单位', '税率', '出库数量',
             '出库金额', '', '含税扣款', '', '工程部位', '自用/班组', '项目名称', '领用人', '备注'),
            ('', '', '', '', '', '', '', '', '', '', '单价', '金额', '是否扣款', '扣款金额', '', '', '', '', ''),
        ))

        # 合并单元格
        table_body[0][0].attr.rowspan = 2
        table_body[0][1].attr.rowspan = 2
        table_body[0][2].attr.rowspan = 2
        table_body[0][3].attr.rowspan = 2
        table_body[0][4].attr.rowspan = 2
        table_body[0][5].attr.rowspan = 2
        table_body[0][6].attr.rowspan = 2
        table_body[0][7].attr.rowspan = 2
        table_body[0][8].attr.rowspan = 2
        table_body[0][9].attr.rowspan = 2
        table_body[0][10].attr.colspan = 2
        table_body[0][12].attr.colspan = 2
        table_body[0][14].attr.rowspan = 2
        table_body[0][15].attr.rowspan = 2
        table_body[0][16].attr.rowspan = 2
        table_body[0][17].attr.rowspan = 2
        table_body[0][18].attr.rowspan = 2

        list_data = []
        outs = OutStore.objects.filter(reciTeam=team_name, store__project__name=project_name)
        # m1 = []
        for o in outs:
            list_data.append((o.date, o.outNo, o.store.mtype, o.store.mclass, o.store.mname, o.store.specifi, '',
                              o.store.unit, '', o.num, o.price, float(o.num)*float(o.price),
                              '-' if o.demount == 0 or o.demount is None else '是',
                              '-' if o.demount is None else o.demount, o.toWhere, o.reciTeam, o.store.project.name,
                              o.receiver, o.remark),)

        # 数据行
        table_body.append_data_rows(list_data)

        # 表格样式，即<table>标签样式
        table_body.set_style({
            'margin': "0 auto",
            'border-collapse': 'collapse',
            'word-break': 'keep-all',
            'white-space': 'nowrap',
            'font-size': '10px',
        })

        # 统一设置所有单元格样式，<td>或<th>
        table_body.set_cell_style({
            'text-align': 'center',
            'border-color': '#000',
            'border-width': '1px',
            'border-style': 'solid',
            'padding': '3px',
            'width': '50px',
        })

        # 表头样式
        table_body.set_header_row_style({
            'color': '#fff',
            # 'background-color': '#48a6fb',
            'background-color': '#4682B4',
            'font-size': '15px',
        })

        # 覆盖表头单元格字体样式
        table_body.set_header_cell_style({
            'padding': '5px',
        })

        # 调小次表头字体大小
        table_body[1].set_cell_style({
            'padding': '4px',
            'font-size': '15px',
        })

        # 遍历数据行，如果增长量为负，标红背景颜色
        for row in table_body.iter_data_rows():
            row.set_style({
                'background-color': 'white',
                'word-break': 'break-all',
                'word-wrap': 'break-word'
            })

        html = table_head.to_html() + table_body.to_html()
        # return HttpResponse(html)
        return JsonResponse({'Content': html}, safe=False)
    return render(request, 'reports/team_details.html')


def provider_details_report(request):
    flag = request.POST.get('csrfmiddlewaretoken')
    if flag:
        # project_name = request.POST.get('project')
        provider = request.POST.get('c_provider')

        # 报表标题
        title = '材料采购明细表'
        table_head = HTMLTable(caption=title)
        table_head.append_data_rows((
            ('', '供货单位：', provider, '', '', '', '', '', '', '', '', '', '',),
        ))
        # 报表头
        # 标题样式
        table_head.caption.set_style({
            'text-align': 'center',
            'font-size': '30px',
        })

        # 表格样式，即<table>标签样式
        table_head.set_style({
            'margin': "0 auto",
            'border-collapse': 'collapse',
            'word-break': 'keep-all',
            'white-space': 'nowrap',
            'font-size': '15px',
        })
        # 统一设置所有单元格样式，<td>或<th>
        table_head.set_cell_style({
            'text-align': 'center',
            'border-color': '#000',
            'border-width': '0px',
            'border-style': 'solid',
            'padding': '8px',
            'min-width': '80px'
        })
        # 字体调整
        table_head[0].set_cell_style({
            'font-weight': '800',
            'border-style': 'solid',
            'padding': '8px',
            'font-size': '15px',
        })

        # 报表主体
        # 标题
        table_body = HTMLTable()

        # 表头行
        table_body.append_header_rows((
            ('日期', '单据编号', '材料类别', '材料小类', '材料名称', '品牌/规格/型号', '厂家名称', '是否结算', '单位', '税率', '数量',
             '材料费', '', '', '', '运杂费', '', '',  # '入库金额', '',
             '项目账目与结算相符', '', '附件数', '采购人', '验收员', '供货单位', '备注'),
            ('', '', '', '', '', '', '', '', '', '', '', '不含税单价', '抵扣税额', '不含税金额', '含税金额', '单价', '金额', '其它',
             # '单价', '金额',
             '其它费用', '合计含税金额', '', '', '', '', ''),
        ))

        # 合并单元格
        table_body[0][0].attr.rowspan = 2
        table_body[0][1].attr.rowspan = 2
        table_body[0][2].attr.rowspan = 2
        table_body[0][3].attr.rowspan = 2
        table_body[0][4].attr.rowspan = 2
        table_body[0][5].attr.rowspan = 2
        table_body[0][6].attr.rowspan = 2
        table_body[0][7].attr.rowspan = 2
        table_body[0][8].attr.rowspan = 2
        table_body[0][9].attr.rowspan = 2
        table_body[0][10].attr.rowspan = 2
        table_body[0][11].attr.colspan = 4
        table_body[0][15].attr.colspan = 3
        table_body[0][18].attr.colspan = 2
        table_body[0][20].attr.rowspan = 2
        table_body[0][21].attr.rowspan = 2
        table_body[0][22].attr.rowspan = 2
        table_body[0][23].attr.rowspan = 2
        table_body[0][24].attr.rowspan = 2

        list_data = []
        instores = InStore.objects.filter(provider=provider)
        # m1 = []
        for o in instores:
            list_data.append((o.date, o.receiptNo, o.mtype, o.mclass, o.mname, o.specifi, '',
                              '', o.unit, '', o.num, float(o.materialfee)/float(o.num),
                              float(o.materialfee)-float(o.num) * float(o.price), float(o.num) * float(o.price),
                              float(o.materialfee), '-', '-', '-', '-', '-', '-', o.buyer, o.inspector,
                              o.provider, o.remark), )

        # 数据行
        table_body.append_data_rows(list_data)

        # 表格样式，即<table>标签样式
        table_body.set_style({
            'margin': "0 auto",
            'border-collapse': 'collapse',
            'word-break': 'keep-all',
            'white-space': 'nowrap',
            'font-size': '10px',
        })

        # 统一设置所有单元格样式，<td>或<th>
        table_body.set_cell_style({
            'text-align': 'center',
            'border-color': '#000',
            'border-width': '1px',
            'border-style': 'solid',
            'padding': '3px',
            'width': '50px',
        })

        # 表头样式
        table_body.set_header_row_style({
            'color': '#fff',
            # 'background-color': '#48a6fb',
            'background-color': '#4682B4',
            'font-size': '10px',
        })

        # 覆盖表头单元格字体样式
        table_body.set_header_cell_style({
            'padding': '5px',
        })

        # 调小次表头字体大小
        table_body[1].set_cell_style({
            'padding': '4px',
            'font-size': '10px',
        })

        # 遍历数据行，如果增长量为负，标红背景颜色
        for row in table_body.iter_data_rows():
            row.set_style({
                'background-color': 'white',
                'word-break': 'break-all',
                'word-wrap': 'break-word'
            })

        html = table_head.to_html() + table_body.to_html()
        # return HttpResponse(html)
        return JsonResponse({'Content': html}, safe=False)
    return render(request, 'reports/provider_details.html')
