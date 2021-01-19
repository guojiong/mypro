from django.http import JsonResponse
from django.shortcuts import render
from HTMLTable import HTMLTable


# Create your views here.

def totals_page(request):
    return render(request, 'reports/totals.html')


def totals_report(request):
    year_month = request.POST.get('year_month')

    # 报表标题
    title = '重庆明珠建设（集团）有限公司 %s 月材料报表' % year_month
    table_head = HTMLTable(caption=title)
    table_head.append_data_rows((
        ('单位：', '泸州项目', '', '', '', '', '', '', '', '单位：', '元'),
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

    list_data = [
        ('1', '材料', '主要材料', '钢材', 20, 12, '1', 110, 10, 20, 12),
        ('2', '', '', '水泥', -9, 21, '1', 110, 10, 20, 12),
        ('3', '', '', '木材', -9, 21, '1', 110, 10, 20, 12),
        ('4', '', '', '地材', -9, 21, '1', 110, 10, 20, 12),
        ('5', '', '', '沥青', -9, 21, '1', 110, 10, 20, 12),
        ('6', '', '', '商混', -9, 21, '1', 110, 10, 20, 12),
        ('7', '', '结构件', '水泥制品', -9, 21, '1', 110, 10, 20, 12),
        ('8', '', '', '钢结构制品', -9, 21, '1', 110, 10, 20, 12),
        ('9', '', '', '木制品', -9, 21, '1', 110, 10, 20, 12),
        ('7', '', '其他材料', '水电材料', -9, 21, '1', 110, 10, 20, 12),
        ('8', '', '', '五金材料', -9, 21, '1', 110, 10, 20, 12),
        ('9', '', '', '化工材料', -9, 21, '1', 110, 10, 20, 12),
        ('', '', '材料小计', '', 10, 21, '1', 110, 10, 20, 12),
        ('10', '（方）辅助材料', 50, '安全文明施工物资', 10, 21, '1', 110, 10, 20, 12),
        ('11', '周转材料', 50, '模板', 10, 21, '1', 110, 10, 20, 12),
        ('12', '', '', '支架', 10, 21, '1', 110, 10, 20, 12),
        ('13', '', '', '扣件', 10, 21, '1', 110, 10, 20, 12),
        ('14', '', '', '其他周材', 10, 21, '1', 110, 10, 20, 12),
        ('15', '', '', '周材小计', 10, 21, '1', 110, 10, 20, 12),
        ('16', '机械设备', 50, '机械设备', 10, 21, '1', 110, 10, 20, 12),
        ('17', '', 50, '设备配件', 10, 21, '1', 110, 10, 20, 12),
        ('18', '', 50, '其他配件', 10, 21, '100', 110, 10, 20, 12),
        ('19', '', 50, '柴油', 10, 21, '100', 110, 10, 20, 12),
        ('20', '', 50, '气油', 10, 21, '100', 110, 10, 20, 12),
        ('21', '', 50, '机械小计', 10, 21, '100', 110, 10, 20, 12),
        ('22', '工器具及低值易耗品', 50, '劳保用品', 10, 21, '100', 110, 10, 20, 12),
        ('23', '', 50, '工器具', 10, 21, '100', 110, 10, 20, 12),
        ('24', '', 50, '管理用具', 10, 21, '100', 110, 10, 20, 12),
        ('25', '', 50, '低值易耗品', 10, 21, '100', 110, 10, 20, 12),
        ('26', '', 50, '低耗品小计', 10, 21, '100', 110, 10, 20, 12),
        ('27', '', '', '安全文明施工物资', 10, 21, '100', 110, 10, 20, 12),
        ('28', '办公物资', '', '办公用品', 10, 21, '100', 110, 10, 20, 12),
        ('29', '', '', '办公设备', 10, 21, '100', 110, 10, 20, 12),
        ('30', '', '', '办公小计', 10, 21, '100', 110, 10, 20, 12),
        ('合计', '', '', '', 10, 21, '100', 110, 10, 20, 12)
    ]

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
        'width': '70px',
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
        if row[2].value == '主要材料':
            row[2].attr.rowspan = 6
        if row[2].value == '结构件':
            row[2].attr.rowspan = 3
        if row[2].value == '其他材料':
            row[2].attr.rowspan = 3
        if row[1].value == '（方）辅助材料':
            row[1].attr.colspan = 3
        if row[1].value == '（方）辅助材料':
            row[1].attr.colspan = 3

        if row[1].value == '周转材料':
            row[1].attr.colspan = 2
            row[1].attr.rowspan = 5
        if row[1].value == '机械设备':
            row[1].attr.colspan = 2
            row[1].attr.rowspan = 6
        if row[1].value == '工器具及低值易耗品':
            row[1].attr.colspan = 2
            row[1].attr.rowspan = 5
        if row[1].value == '办公物资':
            row[1].attr.colspan = 2
            row[1].attr.rowspan = 3

        if row[1].value == '材料':
            row[1].attr.rowspan = 13
        if row[0].value == '合计':
            row[0].attr.colspan = 4

        row.set_style({
            'background-color': 'white',
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
    # return HttpResponse(html)
    return JsonResponse({'Content': html}, safe=False)
