# -*- coding: utf-8 -*-
from openerp import http

# class Licoresreyes(http.Controller):
#     @http.route('/licoresreyes/licoresreyes/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/licoresreyes/licoresreyes/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('licoresreyes.listing', {
#             'root': '/licoresreyes/licoresreyes',
#             'objects': http.request.env['licoresreyes.licoresreyes'].search([]),
#         })

#     @http.route('/licoresreyes/licoresreyes/objects/<model("licoresreyes.licoresreyes"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('licoresreyes.object', {
#             'object': obj
#         })