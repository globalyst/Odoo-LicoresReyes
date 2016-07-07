# -*- coding: utf-8 -*-
{
    'name': "partner_discount",

    'summary': """
        Módulo que permmite crear descuentos para clientes y grupos de clientes """,

    'description': """
        Se pueden aplicar tres tipos de descuentos:
		- Descuento porcentual
		- Descuento fijo
		- Precio fijo
		
		En caso de aplicarse a un grupo de clientes, estos descuentos se aplicarán también a aquellos clientes pertenecientes a dicho grupo.
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
		"views/discounts.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
	'installable': True,
    'auto_install': False,
    'application': True,
}