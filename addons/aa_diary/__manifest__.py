# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : '日记',
    'version' : '1',
    'sequence': 1,
    'category': '日记',
    'website' : 'https://www.andrewl.xyz/',
    'summary' : '日记',
    'description' : """日记""",
    'depends': [
        'base', 'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'views/diary.xml',
        'views/diary_template.xml',
        'data/diary_data.xml',
    ],
    'installable': True,
    'application': True,
}
