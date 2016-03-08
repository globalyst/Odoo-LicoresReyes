import logging
from openerp import models, fields, api, exceptions

_logger = logging.getLogger(__name__)

class OfferSaleOrderLine(models.Model):
	_name = 'offer.sale.order.line'
	sale_order_ref = fields.Many2one('sale.order',ondelete='set null', string="Sale Order", index=True) 
	offer_ref = fields.Many2one('offer',ondelete='set null', string="Oferta", index=True) 
	is_active = fields.Boolean(default=True,string='Activo')
	accumulations = fields.Float(digits=(6, 2), help="Acumulaciones")
	@api.multi
	def unlink(self):
		_logger.warning("WOOOOOO OfferSaleOrderLine unlink DELETEEEEE ")
		return models.Model.unlink(self)

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	offers_lines = fields.One2many('offer.sale.order.line','sale_order_ref', string="Lineas de Ofertas")

	@api.multi
	def onchange_offers_lines(self):
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
					self.offers_lines += self.env['offer.sale.order.line'].new({'is_active': True, 'offer_ref': offer, 'accumulations' : is_offer})
			
			for offer in self.offers_lines:
				_logger.warning("POST LINEAS DE OFERTAS: ID : {0} ; is_active : {1} ; offer_ref : {2} ; accumulations : {3} ; ".format(offer.id,offer.is_active, offer.offer_ref.id, offer.accumulations))						
	
class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	@api.multi
	def set_price(self):
		_logger.warning("sale.order.line set_price")
		self.price_unit = 2.23
	
	@api.onchange('order_id.offers_lines')
	def calcule_price(self):
		_logger.warning("sale.order.line calcule_price	 wwwwwwwwwwwwwwwwwwwwwwwwwwoooooooooooooooooooooooooooooooooooooo")
		
	@api.onchange('product_id')
	def _onchange_product(self):
		self.price_unit = 2.1
		_logger.warning("sale.order.line _onchange_product")
	
	@api.onchange('price_subtotal')
	def _onchange_price_subtotal(self):
		self.price_unit = 2.3
		_logger.warning("sale.order.line _onchange_price_subtotal")
    
	@api.multi
	def product_id_change(self, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False,name='', partner_id=False, lang=False, update_tax=True,date_order=False, packaging=False, fiscal_position=False, flag=False):
		res = super(SaleOrderLine, self).product_id_change(pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,name=name, partner_id=partner_id, lang=lang, update_tax=update_tax,date_order=date_order, packaging=packaging,fiscal_position=fiscal_position, flag=flag) 
		_logger.warning("WOOOOOO product_id_change INIT")

		return res