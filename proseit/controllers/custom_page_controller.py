from odoo import http, _
from odoo.http import request

class Custom_Page_Controller(http.Controller):

    @http.route('/', auth='public', website=True)
    def homepage(self, **kwargs):
        return request.render('proseit.index', {})

    @http.route(['/register'], type='http', auth="public", website=True)
    def registration_choice(self, **kw):
        """Render the registration choice page"""
        return request.render('proseit.registration_choice_template')

    @http.route(['/about'], type='http', auth="public", website=True)
    def aboutpage(self, **kw):
        """Render the about us page"""
        return request.render('proseit.about_page')