# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, fields, _
from odoo.http import request


class WorkOut(http.Controller):
    @http.route(['/work_out'], type='http', auth="public", website=True, methods=['POST', 'GET'])
    def work_out(self, **kw):
        if request.env.uid == request.env.ref('base.public_user').id:
            get_param = request.env['ir.config_parameter'].sudo().get_param
            context = {
                'signup_enabled': get_param('auth_signup.allow_uninvited') == 'True',
                'reset_password_enabled': get_param('auth_signup.reset_password') == 'True',
            }
            return request.render('web.login', context)
        values = {}
        items = request.env['work.out.item'].sudo().search([])
        data = []
        for i in items:
            data.append({
                'name': i.work_out_part.name + '-' + i.name,
                'id': i.id,
            })
        values['items'] = data

        work_out = request.env['work.out'].sudo().search([('user_id', '=', request.env.uid), ('date', '=', fields.Datetime.now()[0:10])], limit=1)
        if kw.get('item_id') and kw.get('weight') and kw.get('times'):
            if not work_out:
                work_out = request.env['work.out'].create({'user_id': request.env.uid})
            line_data = {
                'work_out': work_out.id,
                'part_id': request.env['work.out.item'].search([('id', '=', int(kw.get('item_id')))]).work_out_part.id,
                'item_id': int(kw.get('item_id')),
                'weight': kw.get('weight'),
                'times': int(kw.get('times')),
            }
            request.env['work.out.line'].create(line_data)
        work_out_lines = work_out.line_ids
        values['work_out_lines'] = work_out_lines
        values['select_item_id'] = int(kw.get('item_id')) if kw.get('item_id') else 0
        return request.render("aa_work_out.index", values)