# -*- encoding=utf-8 -*-

from odoo.http import Controller, request, route
import xlwt
import datetime
from cStringIO import StringIO


class DTaskHttp(Controller):

    @route(['/web/export/project_weekly'], type='http', methods=['GET', 'POST'], auth='public',
           website=True)
    def export_weekly(self, **kwargs):
        # 设置字体
        font = xlwt.Font()
        font.bold = True
        font.height = 320
        font1 = xlwt.Font()
        font1.height = 320
        font2 = xlwt.Font()
        font2.height = 320
        font3 = xlwt.Font()
        font3.height = 320
        font3.colour_index = 2
        # 设置背景颜色
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = 22
        # 设置边框
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        # 设置居中
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
        alignment.vert = xlwt.Alignment.VERT_TOP  # 垂直方向
        # 设置居中自动换行
        alignment0 = xlwt.Alignment()
        alignment0.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
        alignment0.vert = xlwt.Alignment.VERT_CENTER  # 垂直方向
        alignment0.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        # 设置左对齐
        alignment1 = xlwt.Alignment()
        alignment1.horz = xlwt.Alignment.HORZ_LEFT
        alignment1.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        # 定义不同的excel style
        # style0: 项目进度
        style0 = xlwt.XFStyle()
        style0.borders = borders
        style0.font = font2
        style0.alignment = alignment0
        style01 = xlwt.XFStyle()
        style01.borders = borders
        style01.font = font3
        style01.alignment = alignment0
        # style1: 导出时间
        style1 = xlwt.XFStyle()
        style1.borders = borders
        style1.font = font1
        # style2: 项目名称
        style2 = xlwt.XFStyle()
        style2.borders = borders
        style2.alignment = alignment
        style2.font = font
        # style3: 项目详细
        style31 = xlwt.XFStyle()
        style31.borders = borders
        style31.alignment = alignment
        style31.font = font1
        style31.pattern = pattern

        # style3: 项目详细
        style3 = xlwt.XFStyle()
        style3.borders = borders
        style3.alignment = alignment
        style3.font = font1
        # style4: 项目描述
        style4 = xlwt.XFStyle()
        style4.borders = borders
        style4.alignment = alignment1
        style4.font = font1
        ids = str(kwargs.get('ids', False))[1:-1].split(',')
        ids = [int(id) for id in ids]
        projects = request.env['dtask.project'].search([('id', 'in', ids)])
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('项目进展')
        worksheet1= workbook.add_sheet('项目计划')

        worksheet.write_merge(0, 0, 0, 1, u'导出时间:%s' % datetime.date.today(), style=style1)
        worksheet.col(0).width = 256 * 20
        worksheet.col(1).width = 256 * 60
        worksheet.col(2).width = 256 * 16
        worksheet.col(3).width = 256 * 13
        worksheet.col(4).width = 256 * 20
        worksheet.col(5).width = 256 * 23

        worksheet1.write(0, 0, u'导出时间:%s' % datetime.date.today(), style=style1)
        worksheet1.col(0).width = 256 * 80
        worksheet1.col(1).width = 256 * 30

        today = datetime.date.today()
        last_monday = today - datetime.timedelta(today.weekday() + 7)
        last_friday = today - datetime.timedelta(today.weekday() + 2)
        i = 1
        j = 0
        for project in projects:
            tasks = []
            for task in project.project_task_ids:
                write_date =task.write_date[:10]
                if last_monday <= datetime.datetime.strptime(write_date, "%Y-%m-%d").date():
                    tasks.append(task)
            if len(project.project_description_ids)>0:
                current_project_description = project.project_description_ids[-1]
            if len(tasks) > 0:
                i += 1
                worksheet.write_merge(i, i, 0, 5, u'项目名称:%s' % project.project_name if project.project_name else '',
                                      style=style2)
                i += 1
                worksheet.write(i, 0, u'整体完成度', style=style0)
                worksheet.write(i, 1, current_project_description.completeness, style=style01)
                worksheet.write(i, 2, u'项目概述', style=style0)
                worksheet.write_merge(i, i, 3, 5, current_project_description.project_description, style=style01)
                i += 1
                worksheet.write(i, 0, u'任务id', style=style31)
                worksheet.write(i, 1, u'任务描述', style=style31)
                worksheet.write(i, 2, u'任务类型', style=style31)
                worksheet.write(i, 3, u'执行人', style=style31)
                worksheet.write(i, 4, u'计划完成时间', style=style31)
                worksheet.write(i, 5, u'当前进度', style=style31)
                i += 1
                for task in tasks:
                    if task.task_type == '1':
                        task_type = u'程序开发'
                    elif task.task_type == '2':
                        task_type = u'外围集成'
                    elif task.task_type == '3':
                        task_type = u'环境搭建'
                    elif task.task_type == '4':
                        task_type = u'研发'
                    elif task.task_type == '5':
                        task_type = u'UI设计'
                    elif task.task_type == '6':
                        task_type = u'样式实现'
                    elif task.task_type == '7':
                        task_type = u'文档与方案'
                    elif task.task_type == '8':
                        task_type = u'项目实施'
                    elif task.task_type == '9':
                        task_type = u'BUG解决'
                    elif task.task_type == '10':
                        task_type = u'其他'
                    recent_progress = dict(task._fields['recent_progress'].selection).get(task.recent_progress, '')
                    worksheet.write(i, 0, task.id if task.id else '', style=style3)
                    worksheet.write(i, 1, task.task_description if task.task_description else '', style=style4)
                    worksheet.write(i, 2, task_type, style=style3)
                    worksheet.write(i, 3, task.performer.name if task.performer else '', style=style3)
                    worksheet.write(i, 4, task.deadline if task.deadline else '', style=style3)
                    worksheet.write(i, 5, recent_progress, style=style3)

                    i += 1
                i += 1
                j += 1
                worksheet1.write_merge(j, j, 0, 1, u'项目名称:%s' % project.project_name if project.project_name else '',
                                      style=style2)
                j += 1
                worksheet1.write(j, 0, u'里程碑', style=style31)
                worksheet1.write(j, 1, u'计划截止时间', style=style31)
                j += 1
                for plan in project.plan_ids:
                    worksheet1.write(j, 0, plan.milestone_id.milestone if plan.milestone_id.milestone else '', style=style3)
                    worksheet1.write(j, 1, plan.deadline if plan.deadline else '', style=style3)
                    j += 1



        name = u'项目周报-' + datetime.date.today().strftime('%y%m%d') + '.xls'
        fp = StringIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        return request.make_response(data, headers=[
            ('Content-Disposition', request.registry['ir.http'].content_disposition(name)),
            ('Content-Type', 'application/vnd.ms-excel')])
