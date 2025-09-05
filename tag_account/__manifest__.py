# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2021-Today Akram Alfusayal
#    license AGPL-3
##############################################################################

{
    'name': "Tag (Account)",

    'summary': """
        Addon to integrate Tag in accounting
    """,

    'author': "Akram Alfusayal",
    'category': 'Akram/',
    'version': "18.0.3.0",
    "depends": ["account", "tag"],
    "data": [
        'data/tag_category.xml',
        'views/account_move.xml',
        'views/tag_view.xml',
    ],
    'images': ['static/description/banner.png'],
    "installable": True,
    "auto_install": False,
    'license': 'LGPL-3',
}
