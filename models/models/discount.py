import logging
from openerp import models, fields, api, exceptions

_logger = logging.getLogger(__name__)

class Discount(models.Model):
	_name = 'discount.line'
	is_active = fields.Boolean(default=True,string='Activo')
	product_id = fields.Many2one('product.product',ondelete='set null', string="Producto a descontar", index=True)
	percentage = fields.Float(digits=(6, 2), string="Descuento (%)")
	fix_discount = fields.Float(digits=(6, 2), string="Descuento fijo")
	fix_price = fields.Float(digits=(6, 2), string="Precio fijo")
	partner_ref = fields.Many2one('res.partner',ondelete='set null', string="Partner", index=True) 
	
class res_partner(models.Model):
	_inherit = 'res.partner'
	
	discount_lines = fields.One2many('discount.line','partner_ref', string="Lineas de Descuento")
	partner_group = fields.Many2one('res.partner', 'Grupo de terceros')
	is_group = fields.Boolean('Is a Group', help="Comprueba si el tercero es un grupo")