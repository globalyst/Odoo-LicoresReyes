from openerp import models, fields, api, exceptions

class DiscountTemplate(models.Model):
	_name = 'discount.template'
	name = fields.Char(string='Template Name')
	discount_lines = fields.One2many('discount','template_ref', string="Discount Lines")
	partner_ref = fields.Many2one('res.partner',ondelete='set null', string="Partner", index=True)
	start_date = fields.Date(default=fields.Date.today,string='Fecha de Inicio')
	end_date = fields.Date(string='Fecha de Fin')
	is_active = fields.Boolean(default=True,string='Activo')
	
class Discount(models.Model):
	_name = 'discount'
	is_active = fields.Boolean(default=True,string='Active')
	product_id = fields.Many2one('product.product',ondelete='set null', string="Product to discount", index=True)
	percentage = fields.Float(digits=(6, 2), string="Discount(%)")
	fix_discount = fields.Float(digits=(6, 2), string="Fix discount")
	fix_price = fields.Float(digits=(6, 2), string="Fix Price")

	template_ref = fields.Many2one('discount.template',ondelete='set null', string="Template", index=True) 
	