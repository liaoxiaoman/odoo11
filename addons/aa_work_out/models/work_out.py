# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class WorkOut(models.Model):
    _name = 'work.out'
    _rec_name = 'date'
    _order = 'id desc'

    date = fields.Date(u'日期', default=lambda self: fields.Datetime.now())
    line_ids = fields.One2many('work.out.line', 'work_out', string=u'明细')
    user_id = fields.Many2one('res.users', string=u'用户', required=True)


class WorkOutLine(models.Model):
    _name = 'work.out.line'

    work_out = fields.Many2one('work.out', string=u'记录')
    part_id = fields.Many2one('work.out.part', string=u'部位')
    item_id = fields.Many2one('work.out.item', string=u'动作')
    weight = fields.Selection([('0.3', u'很轻松的热身组'), ('0.8', u'做完12到16个很累'),
                               ('1', u'八个左右就已经力竭了'), ('1.5', u'拼了老命才做了几个')], u'重量', default='1')
    times = fields.Integer(u'次数')
    total = fields.Float(u'总量', compute="_compute_total")

    @api.onchange('part_id')
    def _onchange_item_id(self):
        if self.part_id:
            return {'domain': {'item_id': [('work_out_part', '=', self.part_id.id)]}}
        else:
            return {'domain': {'item_id': [('work_out_part', '=', 0)]}}

    @api.depends('weight', 'times')
    def _compute_total(self):
        for line in self:
            line.total = float(line.weight) * line.times * line.item_id.score

class WorkOutPart(models.Model):
    _name = 'work.out.part'

    name = fields.Char(u'部位名称')
    items = fields.One2many('work.out.item', 'work_out_part', string=u'动作名称')


class WorkOutItem(models.Model):
    _name = 'work.out.item'

    name = fields.Char(u'动作名称')
    score = fields.Integer(u'评分')
    work_out_part = fields.Many2one('work.out.part', string=u'部位')