# -*- coding: utf-8 -*-
{
    'name': "offers",

    'summary': """ Ofertas de venta """,

    'description': """
       Configura diferentes ofertas de venta.
    """,

    'author': "Álvaro Parra Caro",
    'website': "http://www.jaqueasesores.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/offer.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}