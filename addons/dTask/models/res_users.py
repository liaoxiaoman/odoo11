# -*- encoding=utf-8 -*-
from odoo import models, api, fields


class Users(models.Model):
    _inherit = 'res.users'

    employee_id = fields.Many2one('hr.employee', string='Employee')

    @api.model
    def create(self, vals):
        result = super(Users, self).create(vals)
        e = self.env['hr.employee'].create({'name': result.name})
        result.employee_id = e.id
        return result

    @api.multi
    def unlink(self):
        for s in self:
            s.employee_id.unlink()
        return super(Users, self).unlink()
