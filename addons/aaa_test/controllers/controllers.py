# -*- coding: utf-8 -*-
from odoo import http

class AaaTest(http.Controller):
    @http.route('/aaa_test/aaa_test', auth='public')
    def index(self, **kw):
        print("ghggg")
        return http.request.render('aaa_test.hello', {
            'words': "Hello, world"
        })
    #
    # @http.route('/aaa_test/aaa_test/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('aaa_test.listing', {
    #         'root': '/aaa_test/aaa_test',
    #         'objects': http.request.env['aaa_test.aaa_test'].search([]),
    #     })
    #
    # @http.route('/aaa_test/aaa_test/objects/<model("aaa_test.aaa_test"):obj>/', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('aaa_test.object', {
    #         'object': obj
    #     })