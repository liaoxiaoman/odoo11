# -*- coding: utf-8 -*-

from odoo import models, fields, api

class task_task(models.Model):
    _name = 'task.task'

    task_project = fields.Many2one('task.project', string=u'所属项目')
    task_description = fields.Text(u'任务描述')
    act_user = fields.Many2one('res.users', string=u'执行人')
    check_user = fields.Many2one('res.users', string=u'审核人')
    plan_date = fields.Date(u'计划完成日期', default=lambda self: fields.Datetime.now())
    priority = fields.Selection([('low', '低'), ('normal', '中'), ('high', '高')], string=u'优先级')
    type = fields.Selection([('1', '程序开发'), ('2', '文档撰写'), ('3', 'ui设计'), ('4', 'bug修改')], string=u'任务分类')
    note = fields.Text(u'备注')
    state = fields.Selection([('a', '待执行'), ('b', '待提交'), ('c', '待验证'), ('d', '关闭')], string=u'状态', default='a')

    @api.multi
    def done(self):
        self.write({'state': 'b'})
        return

class task_project(models.Model):
    _name = 'task.project'

    name = fields.Char(u'项目名称')
    manager = fields.Many2one('res.users', string=u'项目经理')
    note = fields.Text(u'备注')
    des_ids = fields.One2many('task.project.des', 'project_id', string=u'项目进度')

class task_project_des(models.Model):
    _name = 'task.project.des'

    date = fields.Date(u'日期')
    des = fields.Selection([('1', '20%'), ('2', '50%'), ('3', '70%'), ('4', '99%'), ('5', '100%')], string=u'进度')
    note = fields.Text(u'描述')
    project_id = fields.Many2one('task.project', string=u'项目id')
