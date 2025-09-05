# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2021-Today Akram Alfusayal
#    license AGPL-3
##############################################################################

{
    'name': "Tag (Product)",

    'summary': """
        Addon to integrate Tag in product
    """,

    'author': "Akram Alfusayal",
    'category': 'Akram/',
    'version': "18.0.3.0",

    "depends": ["product", "tag"],

    "data": [
        'data/tag_category.xml',
        'views/product.xml',
        'views/tag_product.xml'
    ],
    'images': ['static/description/banner.png'],
    "installable": True,
    "auto_install": False,
    'license': 'LGPL-3',
}
