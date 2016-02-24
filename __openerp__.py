# -*- coding: utf-8 -*-
{
    'name': "LicoresReyes",

    'summary': """
        Este módulo pretende resolver los problemas de tarificación de LicoresReyes""",

    'description': """
        Este módulo pretende resolver los problemas de tarificación de LicoresReyes, en primer lugar vamos a añadir una vista que nos permita importar un fichero con los elementos de tarifa.
    """,

    'author': "Álvaro Parra Caro",
    'website': "http://www.jaqueasesores.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '8.0',

    # any module necessary for this one to work correctly
    'depends': [
			'base',
			'sale',
			'product',
	],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
		"views/elementos_de_tarifa.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}