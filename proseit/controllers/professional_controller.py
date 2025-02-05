from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers import portal

class ProfessionalController(http.Controller):

    @http.route(['/professionals', '/professionals/page/<int:page>'], type='http', auth='public', website=True)
    def professionals(self, page=1, search=None, **kw):
        professionals_per_page = 30
        
        domain = []
        if search:
            domain = ['|', ('name', 'ilike', search), ('technical_skills.name', 'ilike', search), ('soft_skills.name', 'ilike', search)]

        Professional = request.env['proseit.professional'].sudo()
        total_professionals = Professional.search_count(domain)
        
        pager = portal.pager(
            url="/professionals",
            url_args={'search': search},
            total=total_professionals,
            page=page,
            step=professionals_per_page
        )

        professionals = Professional.search(domain, limit=professionals_per_page, offset=pager['offset'])
        
        # Preload skills to avoid lazy loading issues
        professionals.sudo().read(['technical_skills', 'soft_skills'])

        return request.render('proseit.professionals_listing_template', {
            'professionals': professionals,
            'search': search,
            'pager': pager,
        })

    @http.route(['/professional/<int:professional_id>'], type='http', auth='public', website=True)
    def professional_detail(self, professional_id, **kw):
        professional = request.env['proseit.professional'].sudo().browse(professional_id)
        if not professional:
            return request.not_found()

        # Preload skills to avoid lazy loading issues
        professional.sudo().read(['technical_skills', 'soft_skills'])

        return request.render('proseit.professional_detail_template', {
            'professional': professional,
        })