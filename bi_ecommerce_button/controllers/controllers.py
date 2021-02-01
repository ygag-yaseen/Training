# -*- coding: utf-8 -*-
# from odoo import http


# class BiEcommerceButton(http.Controller):
#     @http.route('/bi_ecommerce_button/bi_ecommerce_button/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bi_ecommerce_button/bi_ecommerce_button/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bi_ecommerce_button.listing', {
#             'root': '/bi_ecommerce_button/bi_ecommerce_button',
#             'objects': http.request.env['bi_ecommerce_button.bi_ecommerce_button'].search([]),
#         })

#     @http.route('/bi_ecommerce_button/bi_ecommerce_button/objects/<model("bi_ecommerce_button.bi_ecommerce_button"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bi_ecommerce_button.object', {
#             'object': obj
#         })
