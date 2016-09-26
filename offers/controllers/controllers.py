# -*- coding: utf-8 -*-
from openerp import http

# class Offers(http.Controller):
#     @http.route('/offers/offers/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/offers/offers/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('offers.listing', {
#             'root': '/offers/offers',
#             'objects': http.request.env['offers.offers'].search([]),
#         })

#     @http.route('/offers/offers/objects/<model("offers.offers"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('offers.object', {
#             'object': obj
#         })