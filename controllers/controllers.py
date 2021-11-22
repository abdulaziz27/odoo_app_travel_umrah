# -*- coding: utf-8 -*-
from odoo import http

# class Travelumroh(http.Controller):
#     @http.route('/travelumroh/travelumroh/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/travelumroh/travelumroh/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('travelumroh.listing', {
#             'root': '/travelumroh/travelumroh',
#             'objects': http.request.env['travelumroh.travelumroh'].search([]),
#         })

#     @http.route('/travelumroh/travelumroh/objects/<model("travelumroh.travelumroh"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('travelumroh.object', {
#             'object': obj
#         })