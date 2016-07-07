import logging
from openerp import models, fields, api, exceptions

_logger = logging.getLogger(__name__)

class res_partner(models.Model):
	_inherit = 'res.partner'
	
	templates = fields.One2many('discount.template','partner_ref', string="Discount Templates")
	partner_group = fields.Many2one('res.partner', 'Partner Group')
	is_group = fields.Boolean('Is a Group', help="Check if partner is a group")
	
	def getActiveTemplates(self):
		now = fields.Date.today()
		_logger.warning("getActiveTemplates() --> LEN : {0} ;".format(len(self.templates)))	
		active_template = self.templates.search([('start_date','<=',now), ('end_date','>=',now),('is_active','=',True),('partner_ref','=',self.id)])
		_logger.warning("getActiveTemplates() --> LEN : {0} ;".format(len(active_template)))	
		return active_template