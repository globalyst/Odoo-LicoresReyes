# -*- coding: utf-8 -*-
{
    'name': "product_offers",

    'summary': """
        Módulo que permmite crear ofertas en base a unos requerimientos, que en caso de cumplirse se aplicarán una serie de descuentos, regalos, etc.""",

    'description': """
		Módulo que permmite crear ofertas en base a unos requerimientos, que en caso de cumplirse se aplicarán una serie de descuentos, regalos, etc.
    """,

    'author': "Álvaro Parra Caro",
    'website': "http://www.jaqueasesores.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

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
		"views/offers.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],

}