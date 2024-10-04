# -*- coding: utf-8 -*-
# from odoo import http


# class Proseit(http.Controller):
#     @http.route('/proseit/proseit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/proseit/proseit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('proseit.listing', {
#             'root': '/proseit/proseit',
#             'objects': http.request.env['proseit.proseit'].search([]),
#         })

#     @http.route('/proseit/proseit/objects/<model("proseit.proseit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('proseit.object', {
#             'object': obj
#         })

