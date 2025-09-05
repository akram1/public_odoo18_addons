# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2024-Today Akram Alfusayal
#    license AGPL-3
##############################################################################

{
    'name': "Tag (Partner)",

    'summary': """
        Addon for Tag integration with partner. Enjoy 71 partner tag in 9 categories.
    """,

    'author': "Akram Alfusayal",
    'category': 'Akram/',
    'version': "18.0.3.0",
    "depends": ["contacts", "tag"],
    "data": [
        'data/tag_category_data.xml',
        'data/tag_data.xml',
        'views/partner.xml',
        'views/tag_partner.xml'
    ],
    'images': ['static/description/banner.png'],
    "installable": True,
    "auto_install": False,
    'license': 'LGPL-3',
}
