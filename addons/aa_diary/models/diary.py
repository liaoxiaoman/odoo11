# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Diary(models.Model):
    _name = 'diary'
    _rec_name = 'date'
    _order = 'id desc'

    date = fields.Date(u'日期', default=lambda self: fields.Datetime.now())
    text = fields.Text(u'内容')
    user_id = fields.Many2one('res.users', string=u'用户', required=True)
    comment_ids = fields.One2many('diary.comment', 'diary_id')

class DiaryComment(models.Model):
    _name = 'diary.comment'
    _rec_name = 'date'
    _order = 'id'

    date = fields.Date(u'日期', default=lambda self: fields.Datetime.now())
    text = fields.Text(u'内容')
    user_id = fields.Many2one('res.users', string=u'用户', required=True)
    diary_id = fields.Many2one('diary')