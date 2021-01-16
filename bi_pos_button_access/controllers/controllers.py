# -*- coding: utf-8 -*-
# from odoo import http


# class BiPosButtonAccess(http.Controller):
#     @http.route('/bi_pos_button_access/bi_pos_button_access/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bi_pos_button_access/bi_pos_button_access/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bi_pos_button_access.listing', {
#             'root': '/bi_pos_button_access/bi_pos_button_access',
#             'objects': http.request.env['bi_pos_button_access.bi_pos_button_access'].search([]),
#         })

#     @http.route('/bi_pos_button_access/bi_pos_button_access/objects/<model("bi_pos_button_access.bi_pos_button_access"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bi_pos_button_access.object', {
#             'object': obj
#         })
