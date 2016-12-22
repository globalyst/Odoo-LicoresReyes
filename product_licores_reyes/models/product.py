from openerp import models, fields

class Format(models.Model):
	_name = 'product.format'
	
	name = fields.Char(string='Name')
	description = fields.Char(string='Descripcion')
	capacity = fields.Integer(string='Capacidad',default=0)
	is_default = fields.Boolean(default=True,string='Por defecto')
	
class product_template(models.Model):
	_inherit = 'product.template'
	
	graduacion = fields.Float(digits=(4, 2), string="Graduacion Alcoholica" help="Alcoholic graduation")
	format_id = fields.Many2one('product.format',ondelete='cascade', string="Formato")

