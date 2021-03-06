# -*- coding: utf-8 -*-
{
    'name': "product_licores_reyes",

    'summary': """
        Ampliación del modelo de productos para Licores Reyes""",

    'description': """
        Ampliación del modelo de productos para Licores Reyes, inclyendo graduación alcohólica y formato de producto.
    """,

    'author': "Álvaro Parra Caro",
    'website': "http://www.jaqueasesores.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
		'views/product.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}