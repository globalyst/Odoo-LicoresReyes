import logging
from openerp import models, fields, api, exceptions

_logger = logging.getLogger(__name__)

class OfferSaleOrderLine(models.Model):
	_name = 'offer.sale.order.line'
	sale_order_ref = fields.Many2one('sale.order',ondelete='set null', string="Sale Order", index=True) 
	offer_ref = fields.Many2one('offer',ondelete='set null', string="Oferta", index=True) 
	is_active = fields.Boolean(default=False,string='Activo')
	accumulations = fields.Float(digits=(6, 2), string="Acumulaciones",  help="Acumulaciones")

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

	offers_lines = fields.One2many('offer.sale.order.line','sale_order_ref', string="Lineas de Ofertas")
	discount_lines = fields.One2many('discount.sale.order.line','sale_order_ref', string="Lineas de Descuentos")

	@api.multi
	def apply_discountsAndOffers(self):
		self.apply_discounts()
		self.apply_offers()
		
	
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
		
	
	@api.multi
	def apply_offers(self):
		_logger.warning("SALE ORDER _onchange_offers_lines() INIT ")				
		for offer_line in self.offers_lines:
			if offer_line.is_active:
				offer = offer_line.offer_ref
				for gift in offer.gift_id:
					for gift_line in gift.giftline_id:
						is_fix_price = gift_line.fix_price > 0.0

						if is_fix_price:
							_logger.warning("_onchange_offers_lines is_fix_price")	
							for order_line in self.order_line:
								if  gift_line.free_product.id == order_line.product_id.id:
									_logger.warning("applyOffer set fix price FROM {0} TO {1} ".format(order_line.price_unit,gift_line.fix_price))	
									order_line.price_unit = gift_line.fix_price
									#order_line.set_price()
						else:
							val = {
								'name': gift_line.free_product.name,
								'order_id': self.id,
								'product_id': gift_line.free_product.id,
								'product_uom_qty':  gift_line.qty * offer_line.accumulations,
								'product_uom': self.order_line[0].product_uom.id,
								'price_unit': 0.0,
								'state': 'draft',
							}

							self.order_line |= self.env['sale.order.line'].new(val)
							_logger.warning("NUEVA LINEA !!")			

							

	@api.onchange('order_line')
	def _onchange_order_line(self):
		_logger.warning("SALE ORDER _onchange_order_line() INIT offers_lines {0} ; Sale Order ID : {1}".format( len(self.offers_lines),self.id))
					
		if len(self.order_line) > 0:
			
			for line in self.offers_lines:
				self.offers_lines -= line
				
			active_offers = self.env['offer'].getActiveOffers()
			
			for offer in active_offers:
				#_logger.warning("OFERTA ACTIVA: Active {0} ; Desc: {1} ;  START : {2} ; END : {3} ; id : {4}".format(offer.is_active, offer.name, offer.start_date, offer.end_date, offer) )
				
				is_offer = offer.checkPreconditions(self.order_line)
				_logger.warning("SALE ORDER _onchange_order_line() IS OFFER  {0}".format(is_offer))
				
				product_uom = self.order_line[0].product_uom;
				
				if is_offer > 0.0: 
					self.offers_lines += self.env['offer.sale.order.line'].new({'is_active': False, 'offer_ref': offer, 'accumulations' : int(is_offer) })
			
			for offer in self.offers_lines:
				_logger.warning("POST LINEAS DE OFERTAS: ID : {0} ; is_active : {1} ; offer_ref : {2} ; accumulations : {3} ; ".format(offer.id,offer.is_active, offer.offer_ref.id, offer.accumulations))						
	
	
	@api.onchange('partner_invoice_id')
	def onchange_partner_invoice_id(self):
		_logger.warning("SALE ORDER onchange_partner_invoice_id() INIT --> Self : {0} ; Self ID : {1} ; self.discount_lines len : {2} ;".format(self,self.id, len(self.discount_lines)))		

		for line in self.discount_lines:
			self.discount_lines -= line
		
		for record in self:
			_logger.warning("record {0}".format(record))
		
		#sale_order = self.pool.get('sale.order').browse(self,context)
		discount_lines = self.partner_id.discount_lines
		if self.partner_id.partner_group.id != False and len (self.partner_id.partner_group.discount_lines) > 0:
			discount_lines = self.partner_id.partner_group.discount_lines
			
		is_active = (self.partner_id.partner_group.id != False) and (len (self.partner_id.partner_group.discount_lines) > 0)
		for discount in self.partner_id.partner_group.discount_lines:
			self.newDiscount(discount,is_active)

		for discount in self.partner_id.discount_lines:
			self.newDiscount(discount,not is_active)
	
	@api.model
	def newDiscount(self,discount,is_active):
			_logger.warning("SALE ORDER _onchange_partner() Descuento --> Producto : {0} ; percentage : {1} ; fix_price : {2} ; ".format(discount.product_id, discount.percentage , discount.fix_price))		
			val = {
				'product_id': discount.product_id.id,
				'is_active': is_active,
				'percentage': discount.percentage,
				'fix_price':  discount.fix_price,
			}
			
			new_discount = self.env['discount.sale.order.line'].new(val)
			self.discount_lines |= new_discount	
			
			
	class product_pricelist(models.Model):
		_inherit = 'product.pricelist.version'
		
		@api.multi
		def duplicate(self):
			_logger.warning("product_pricelist WOOOOOO Duplicate")
			
			name = " NUEVA VERSION"
			val = {
				'pricelist_id': self.pricelist_id,
				'name': name,
			}
			new_version = self.env['product.pricelist.version'].new(val)
			
			for item in self.items_id:
				val = {
					'base': item.base,
					'base_pricelist_id': item.base_pricelist_id,
					'categ_id': item.categ_id,
					'company_id': item.company_id,
					'min_quantity': item.min_quantity,
					'name': item.name,
					'price_discount': item.price_discount,
					'price_max_margin': item.price_max_margin,
					'price_min_margin': item.price_min_margin,
					'price_round': item.price_round,
					'price_surcharge': item.price_surcharge,
					'price_version_id': item.price_version_id,
					'product_id': item.product_id,
					'sequence': item.sequence,
				}	
				new_item = self.env['product.pricelist.item'].new(val)
				new_version.items_id |= new_item
				
			self.pricelist_id.version_id |= new_version	
			