# -*- coding: utf-8 -*-
from openerp import http

# class PartnerDiscount(http.Controller):
#     @http.route('/partner_discount/partner_discount/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/partner_discount/partner_discount/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('partner_discount.listing', {
#             'root': '/partner_discount/partner_discount',
#             'objects': http.request.env['partner_discount.partner_discount'].search([]),
#         })

#     @http.route('/partner_discount/partner_discount/objects/<model("partner_discount.partner_discount"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('partner_discount.object', {
#             'object': obj
#         })