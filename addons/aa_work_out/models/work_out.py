# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class WorkOut(models.Model):
    _name = 'work.out'

    name = fields.Char(u'名称')
    date = fields.Date(u'日期', default=lambda self: fields.Datetime.now())
    line_ids = fields.One2many('work.out.line', 'work_out', string=u'明细')
    user_id = fields.Many2one('res.users', string=u'用户', required=True)


class WorkOutLine(models.Model):
    _name = 'work.out.line'

    work_out = fields.Many2one('work.out', string=u'记录')
    part_id = fields.Many2one('work.out.part', string=u'部位')
    item_id = fields.Many2one('work.out.item', string=u'动作')
    weight = fields.Float(u'重量')
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
            line.total = line.weight * line.times

class WorkOutPart(models.Model):
    _name = 'work.out.part'

    name = fields.Char(u'部位名称')
    items = fields.One2many('work.out.item', 'work_out_part', string=u'动作名称')


class WorkOutItem(models.Model):
    _name = 'work.out.item'

    name = fields.Char(u'动作名称')
    work_out_part = fields.Many2one('work.out.part', string=u'部位')