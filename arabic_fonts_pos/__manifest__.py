# -*- coding: utf-8 -*-
##############################################################################
#
#    Tirasys
#    Copyright (C) 2024-Today Akram Alfusayal
#    license AGPL-3
##############################################################################

{
    'name': "Odoo Arabic Font for POS",

    'summary': """
        Defult POS font becomes Noto Naskh Arabic font.""",

    'description': """
        Defult font becomes Noto Naskh Arabic font.
    """,
    'author': "Akram Alfusayal",
    'category': 'Tirasys/',
    'version': '18.0.1.0',
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'arabic_fonts_pos/static/src/scss/arabic_fonts.scss',
            'arabic_fonts_pos/static/src/scss/pos_style.scss',
        ],

    },
    'license': 'AGPL-3',
    'auto_install': False,
    'installable': True,
}
