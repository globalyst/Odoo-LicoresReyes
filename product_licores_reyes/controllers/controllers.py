# -*- coding: utf-8 -*-
from openerp import http

# class ProductLicoresReyes(http.Controller):
#     @http.route('/product_licores_reyes/product_licores_reyes/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_licores_reyes/product_licores_reyes/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_licores_reyes.listing', {
#             'root': '/product_licores_reyes/product_licores_reyes',
#             'objects': http.request.env['product_licores_reyes.product_licores_reyes'].search([]),
#         })

#     @http.route('/product_licores_reyes/product_licores_reyes/objects/<model("product_licores_reyes.product_licores_reyes"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_licores_reyes.object', {
#             'object': obj
#         })