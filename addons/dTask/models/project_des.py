# -*- encoding=utf-8 -*-
from odoo import fields, api, models


class dTaskProjectDescription(models.Model):
    _name = 'dtask.project_description'
    _description = u'项目进度描述'
    _rec_name = 'project_id'

    project_id = fields.Many2one('dtask.project', string=u'项目名称')
    time = fields.Date(u'时间')
    completeness = fields.Char(string=u'整体完成度',default=u'%')
    project_description = fields.Text(u'进度描述')
