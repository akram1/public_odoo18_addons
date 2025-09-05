# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2024-Today Akram Alfusayal
#    license AGPL-3
##############################################################################

{
    'name': "Fix RTL Style",

    'summary': """
        This module correct some RTL issues in Odoo""",

    'description': """
        This module correct many RTL issues in Odoo:
        - number representation in RTL mode. Minus sign and other signs are now displayed the same way of LTR and right aligned.
        - Phone number in Partner form in kanban view inside notebook
        - Fix the orientation of Optional Columns Dropdown so it drops to the right side
        - Web Site menu
        - And many others
    """,
    'author': "Akram Alfusayal",
    'category': 'Akram/',
    'version': '18.0.1.0',
    'depends': ['web'],
    'qweb': [],
    'assets': {
        'web.assets_common': [
            'fix_rtl/static/src/css/fix_rtl.css'
        ],
        'web.report_assets_common': [
            'fix_rtl/static/src/css/fix_rtl.css'
        ],
    },
    'data': ['views/fix_rtl.xml'],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'auto_install': False,
    'installable': True,
}
