# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : '健身记录',
    'version' : '1',
    'sequence': 1,
    'category': '健身记录',
    'website' : 'https://www.andrewl.xyz/',
    'summary' : '健身记录',
    'description' : """健身记录""",
    'depends': [
        'base', 'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/work_out.xml',
        'views/work_out_template.xml',
        'data/work_out_data.xml',
    ],
    'installable': True,
    'application': True,
}
