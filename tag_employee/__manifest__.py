# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2021-Today Akram Alfusayal
#    license AGPL-3
##############################################################################

{
    'name': "Tag (Employee)",

    'summary': """
        Addon to integrate Tag in employee. Enjoye 268 eomployee tags in 15 categories.
    """,

    'author': "Akram Alfusayal",
    'category': 'Akram/',
    'version': "18.0.3.0",
    "depends": ["hr", 'tag'],
    "data": [
        'data/tag_category_data.xml',
        'data/tag_data.xml',
        'data/tag_default.xml',
        'views/employee.xml',
        'views/tag_employee.xml'
    ],
    'images': ['static/description/banner.png'],
    "installable": True,
    "auto_install": False,
    'license': 'LGPL-3',
}
