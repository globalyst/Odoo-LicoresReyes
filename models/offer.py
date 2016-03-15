import logging
from openerp import models, fields, api, exceptions

_logger = logging.getLogger(__name__)

class Offer(models.Model):
	_name = 'offer'
	name = fields.Char(string='Oferta')
	is_active = fields.Boolean(default=True,string='Activo')
	supplier_pay = fields.Boolean(default=True,string='A cargo de proveedor')
	start_date = fields.Date(default=fields.Date.today,string='Fecha de Inicio')
	end_date = fields.Date(string='Fecha de Fin')
	qty = fields.Integer(string='Cantidad')
	max_accumulations = fields.Integer(string='Maximo de acumulaciones')
	precondition_id = fields.One2many('offer.precondition','offer_id', string="Precondiciones")
	gift_id = fields.One2many('offer.gift','offer_id', string="Regalos")
	
	@api.model
	def getActiveOffers(self):
		now = fields.Date.today()
		active_offers = self.search([('start_date','<=',now), ('end_date','>=',now),('is_active','=',True)])
		return active_offers
		
	@api.model
	def checkPreconditions(self,order_line):
		result = 0.0
		
		for precondition in self.precondition_id:
			#_logger.warning("checkPreconditions PRECONDITION--> DESC : {0} ; QTY_MIN : {1} ;  PRICE_MIN : {2}".format(precondition.name, precondition.qty_min, precondition.price_min))
			isGlobalPriceMin =  precondition.qty_min > 0.0;
			precondition_result = 0.0
			qty_sum = 0.0
						
			for preconditionline in precondition.preconditionline_id:
				#_logger.warning("checkPreconditions PRECONDITION_LINE --> PRODUCT : {0} ; PRICE_MIN : {1} ;   QTY_MIN : {2} ;".format(preconditionline.paid_product.id,preconditionline.price_min,preconditionline.qty_min))
				precondition_line_result = 0.0
				qty_sum_line = 0.0
				
				for line in order_line:
					#_logger.warning("checkPreconditions ORDER LINE --> PRODUCT : {0} ; PRICE_UNIT : {1} ;   QTY : {2} ; SUBTOTAL : {3}".format(line.product_id.id,line.price_unit,line.product_uom_qty,line.price_subtotal))
					
					is_SameProduct = (line.product_id.id == preconditionline.paid_product.id)
					if is_SameProduct: 
					
						is_MinPrice = (line.price_unit >= precondition.price_min)
						if not isGlobalPriceMin:		 			
							is_MinPrice = (line.price_unit >= preconditionline.price_min)
							
						if is_MinPrice: 
							
							is_MinQuantity = (line.product_uom_qty >= precondition.qty_min)
							if not isGlobalPriceMin:
								is_MinQuantity = (line.product_uom_qty >= preconditionline.qty_min)
							
							qty_sum += line.product_uom_qty							
							if is_MinQuantity:
								qty_sum_line += line.product_uom_qty
								
				if preconditionline.qty_min > 0.0:
					precondition_line_result = qty_sum_line / preconditionline.qty_min
				
				precondition_result += precondition_line_result
			
			if	precondition_result == 0.0 and isGlobalPriceMin:		
				precondition_result = qty_sum / precondition.qty_min
			
			result += precondition_result
			_logger.warning("checkPreconditions PRECONDITION--> RESULT : {0} ; precondition_result : {1} ;  isGlobalPriceMin : {2} ; qty_sum : {3}".format(result, precondition_result,isGlobalPriceMin,qty_sum))
			
		return result
	

class Precondition(models.Model):
	_name = 'offer.precondition'
	
	name = fields.Char(string='Nombre')
	qty_min = fields.Integer(string='Cantidad minima')
	price_min = fields.Float(digits=(6, 2), help="Precio minimo")

	preconditionline_id = fields.One2many('offer.precondition.line','precondition_id', string="Lineas de precondicion")
	offer_id = fields.Many2one('offer',ondelete='cascade', string="Oferta", required=True)
	
class PreconditionLine(models.Model):
	_name = 'offer.precondition.line'
	paid_product = fields.Many2one('product.product',ondelete='set null', string="Producto a pagar", index=True) 
	qty_min = fields.Integer(string='Cantidad minima')
	price_min = fields.Float(digits=(6, 2), string="Precio minimo")
	precondition_id = fields.Many2one('offer.precondition',ondelete='cascade', string="Precondicion", required=True)
		

class Gift(models.Model):
	_name = 'offer.gift'
	name = fields.Char(string='Regalo')
	giftline_id = fields.One2many('offer.gift.line','gift_id', string="Lineas de regalos")
	offer_id = fields.Many2one('offer',ondelete='cascade', string="Oferta", required=True)
	
class GiftLine(models.Model):
	_name = 'offer.gift.line'
	free_product = fields.Many2one('product.product',ondelete='set null', string="Producto a regalar", index=True)
	qty = fields.Integer(string='Cantidad a regalar')
	fix_price = fields.Float(digits=(6, 2), string="Precio fijo")
	gift_id = fields.Many2one('offer.gift',ondelete='cascade', string="Regalo", required=True)
	