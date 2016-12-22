from openerp import models, fields

class Format(models.Model):
	_name = 'product.format'
	
	name = fields.Char(string='Name')
	description = fields.Char(string='Description')
	capacity = fields.Integer(string='Capacity',default=0)
	is_default = fields.Boolean(default=True,string='Por defecto')
	
class product_template(models.Model):
	_inherit = 'product.template'
	
	graduacion = fields.Float(digits=(4, 2), help="Alcoholic graduation")
	format_id = fields.Many2one('product.format',ondelete='cascade', string="Formato")

