# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2024-Today Akram Alfusayal
#    license AGPL-3
##############################################################################

{
    'name': "Odoo Arabic Font for Backend and Front end",

    'summary': """
        Defult font becomes Noto Naskh Arabic font.""",

    'description': """
        Defult font becomes Noto Naskh Arabic font.
    """,
    'author': "Akram Alfusayal",
    'category': 'akram/',
    'version': '18.0.1.0',
    'depends': ['web'],
    'assets': {
        'web.report_assets_common': [
            "arabic_fonts_web/static/src/scss/arabic_fonts.scss",
        ],
        'web.report_assets_pdf': [
            "arabic_fonts_web/static/src/scss/arabic_fonts.scss",
        ],
        'web.assets_backend': [
            'arabic_fonts_web/static/src/scss/web_style.scss',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'auto_install': False,
    'installable': True,
}
