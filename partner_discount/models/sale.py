import logging
from openerp import models, fields, api, exceptions

_logger = logging.getLogger(__name__)

class DiscountSaleOrderLine(models.Model):
	_name = 'discount.sale.order.line'
	sale_order_ref = fields.Many2one('sale.order',ondelete='set null', string="Sale Order", index=True) 
	is_active = fields.Boolean(default=True,string='Activo')	
	product_id = fields.Many2one('product.product',ondelete='set null', string="Producto a descontar", index=True)
	percentage = fields.Float(digits=(6, 2), string="Descuento (%)")
	fix_price = fields.Float(digits=(6, 2), string="Precio fijo")
	fix_discount = fields.Float(digits=(6, 2), string="Descuento fijo")
	
	
class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'
	pricelist_price = fields.Float(digits=(6, 2), string="Precio Tarifa")
	
	@api.multi
	@api.onchange('name')
	def name_change(self):
		_logger.warning("SALE ORDER LINE  _onchange_order_line() Self ID {0} ; Price Unit: {1} ".format(self.id,self.price_unit))
		self.pricelist_price = self.price_unit
		
	
class SaleOrder(models.Model):
	_inherit = 'sale.order'

	discount_lines = fields.One2many('discount.sale.order.line','sale_order_ref', string="Lineas de Descuentos")

	@api.multi
	def apply_discounts(self):
		_logger.warning("SALE ORDER apply_discounts() INIT --> LENGTH DISCOUNT LINES {0} ;  ".format(len(self.discount_lines)))	
		for discount_line in self.discount_lines:
			_logger.warning("SALE ORDER apply_discounts() discount_line --> product {0} ; is_active {1} ; percentage {2} ; fix_price {3} ;  ".format(discount_line.product_id,discount_line.is_active,discount_line.percentage,discount_line.fix_price))	
			if discount_line.is_active:
				for order_line in self.order_line:
					product = order_line.product_id.with_context(
							lang=order_line.order_id.partner_id.lang,
							partner=order_line.order_id.partner_id.id,
							quantity=order_line.product_uom_qty,
							date=order_line.order_id.date_order,
							pricelist=order_line.order_id.pricelist_id.id,
							uom=order_line.product_uom.id
					)
					pricelist_price = product.price
					_logger.warning("SALE ORDER apply_discounts() order_line --> PRICELIST_PRICE {0} ; ".format(pricelist_price))
					order_line.pricelist_price = pricelist_price
					
					if  discount_line.product_id.id == order_line.product_id.id:
						
						_logger.warning("SALE ORDER apply_discounts() order_line --> product : {0} ; price_unit : {1} ; pricelist_price : {2} ; ".format(order_line.product_id.id,order_line.price_unit,order_line.pricelist_price))	
						if discount_line.fix_price > 0.0:
							order_line.price_unit = discount_line.fix_price
							_logger.warning("SALE ORDER apply_discounts() discount_line.fix_price  > 0.0  --> order_line.price_unit : {0}".format(order_line.price_unit))	
						elif discount_line.fix_discount:
							order_line.price_unit = (order_line.pricelist_price - discount_line.fix_discount) 
							_logger.warning("SALE ORDER apply_discounts() discount_line.fix_price  <= 0.0  --> order_line.price_unit : {0}".format(order_line.price_unit))
						else:
							order_line.price_unit = (order_line.pricelist_price * (1 - (discount_line.percentage) / 100.0) )
							_logger.warning("SALE ORDER apply_discounts() discount_line.fix_price  <= 0.0  --> order_line.price_unit : {0}".format(order_line.price_unit))
									
	@api.onchange('partner_invoice_id')
	def onchange_partner_invoice_id(self):
		_logger.warning("SALE ORDER onchange_partner_invoice_id() INIT --> Self : {0} ; Self ID : {1} ; self.discount_lines len : {2} ;".format(self,self.id, len(self.discount_lines)))		

		for line in self.discount_lines:
			self.discount_lines -= line
		
		templates = self.partner_id.getActiveTemplates()
		group_templates = self.partner_id.partner_group.getActiveTemplates()
				
		is_active = (self.partner_id.partner_group.id != False) and ( len(group_templates) > 0)
		
		for template in templates:
			for discount in template.discount_lines:
				self.newDiscount(discount, not is_active)
		
		for template in group_templates:
			for discount in template.discount_lines:
				self.newDiscount(discount, is_active)
		

	@api.model
	def newDiscount(self,discount,is_active):
			val = {
				'product_id': discount.product_id.id,
				'is_active': is_active,
				'percentage': discount.percentage,
				'fix_price':  discount.fix_price,
				'fix_discount': discount.fix_discount,
			}
			
			new_discount = self.env['discount.sale.order.line'].new(val)
			self.discount_lines |= new_discount	
			
			
