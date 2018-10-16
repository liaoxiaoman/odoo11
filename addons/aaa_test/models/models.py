# -*- coding: utf-8 -*-

from odoo import models, fields, api

class aaa_test(models.Model):
    _name = 'aaa_test.aaa_test'
    name = fields.Char(u'名字')
    value = fields.Integer(u'值1')
    value2 = fields.Float(compute="_value_pc", store=True, string=u'值2')
    description = fields.Text()
    file = fields.Binary(u'文件')
    selection = fields.Selection([('1', '第一'), ('2', '第二'), ('3', '第三')], string=u'选择选项')
    bool = fields.Boolean(u'是否')
    date = fields.Date(u'日期（年月日）')
    datetime = fields.Datetime(u'时间')
    html = fields.Html(u'html源码')
    sub_id = fields.Many2one('aaa_test.aaa_test_sub', string=u'子表')
    sub2_id = fields.One2many('aaa_test.aaa_test_sub2', 'test_id')

    @api.model
    def create(self, vals):

        vals['bool'] = True

        res = super(aaa_test, self).create(vals)

        print (res.name)
        # res.write({'bool': True})

        return res

    @api.one
    def write(self, vals):
        res = super(aaa_test, self).write(vals)
        print (self.name)
        test_ids = self.env['aaa_test.aaa_test'].search([('bool', '=', True)])
        return res

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # args.append(('value', '>=', 50))
        # args.append(('bool', '=', True))
        return super(aaa_test, self).search(args=args, offset=offset, limit=limit, order=order, count=count)

    @api.multi
    def unlink(self):
        return super(aaa_test, self).unlink()

    @api.onchange('value', 'name')
    def _onchange_bool(self):
        if self.value > 100 and self.name:
            self.bool = True
        else:
            self.bool = False
        return


    @api.depends('value', 'name')
    def _value_pc(self):
        self.value2 = float(self.value) / 100


class aaa_test_sub(models.Model):
    _name = 'aaa_test.aaa_test_sub'
    _rec_name = 'id'

    name = fields.Char(u'名字')
    code = fields.Char(u'编号')

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        res = []
        for record in self:
            if record.name and record.code:
                name = record.name + '-' + record.code
            else:
                name = str(record.id)
            res.append((record.id, name))
        return res

class aaa_test_sub2(models.Model):
    _name = 'aaa_test.aaa_test_sub2'
    name = fields.Char(u'名字')
    test_id = fields.Many2one('aaa_test.aaa_test', string=u'主表')

class aaa_test_new(models.Model):
    _name = 'aaa_test.aaa_test.new'
    _inherit = ['aaa_test.aaa_test']

    new_name = fields.Char(u'new_name')

class aaa_test_new2(models.Model):
    _inherit = 'aaa_test.aaa_test'
    _order = 'value desc, value2'

    new_name = fields.Char(u'new_name')
    new_name2 = fields.Char(u'new_name2')