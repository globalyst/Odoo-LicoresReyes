# -*- coding: utf-8 -*-
from openerp import http

# class ProductOffers(http.Controller):
#     @http.route('/product_offers/product_offers/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_offers/product_offers/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_offers.listing', {
#             'root': '/product_offers/product_offers',
#             'objects': http.request.env['product_offers.product_offers'].search([]),
#         })

#     @http.route('/product_offers/product_offers/objects/<model("product_offers.product_offers"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_offers.object', {
#             'object': obj
#         })