# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, fields, _
from odoo.http import request
import json

class Diary(http.Controller):
    @http.route(['/diary'], type='http', auth="public", website=True, methods=['POST', 'GET'])
    def diary(self, **kw):
        # 验证登录
        if request.env.uid == request.env.ref('base.public_user').id:
            get_param = request.env['ir.config_parameter'].sudo().get_param
            context = {
                'signup_enabled': get_param('auth_signup.allow_uninvited') == 'True',
                'reset_password_enabled': get_param('auth_signup.reset_password') == 'True',
            }
            return request.render('web.login', context)
        if request.env.uid in [8, 6]:
            if kw.get('text'):
                if not request.env['diary'].sudo().search([('text', '=', kw.get('text'))]):
                    diary_data = {
                        'text': kw.get('text'),
                        'user_id': request.env.uid,
                    }
                    request.env['diary'].create(diary_data)
            values = {}
            diarys = request.env['diary'].sudo().search([])
            data = []
            for i in diarys:
                data.append({
                    'date': i.date[5:],
                    'id': i.id,
                    'text': i.text[0:12]+'...',
                    'user': i.user_id.name,
                })
            values['diarys'] = data
            return request.render("aa_diary.index", values)
        else:
            return request.redirect('/contactus')

    @http.route(['/get_details/<int:detail_id>'], type='http', auth="public", website=True, methods=['POST', 'GET'])
    def get_details(self, detail_id, **kw):
        detail = request.env['diary'].sudo().browse(detail_id).text
        return request.render("aa_diary.detail", {'detail': detail})