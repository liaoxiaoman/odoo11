# -*- coding: utf-8 -*-
# author:xuwentao
{
    'name': 'dTask',
    'version': '1.0',
    'sequence': 1,
    'summary': '任务看板',
    'description': """
    """,
    'author': '北京迪威特',
    'website': 'http://www.bjdvt.com',
    'depends': ['hr', 'base'],
    'data': ['security/ir.model.access.csv',
             'views/task.xml',
             'views/project_description.xml',
             'views/plan.xml',
             'views/project.xml',
             'views/task-ref.xml',
             ],
    'installable': True,
    'application': True,
}
