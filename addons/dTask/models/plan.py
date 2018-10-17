# -*- encoding=utf-8 -*-
from odoo import fields, api, models


class dTaskPlan(models.Model):
    _name = 'dtask.plan'
    _description = u'计划'

    project_id = fields.Many2one('dtask.project', string=u'项目名称')
    milestone_id = fields.Many2one('dtask.milestone',u'里程碑')
    deadline = fields.Date(u'截止时间')

class milestone(models.Model):
    _name = 'dtask.milestone'
    _description = u'里程碑'
    _rec_name = u'milestone'

    milestone=fields.Char(u'里程碑')