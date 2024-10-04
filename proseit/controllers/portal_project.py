from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class PortalProjects(CustomerPortal):

    @http.route(['/my/projects'], type='http', auth="user", website=True)
    def my_projects(self, **kw):
        # Get the logged-in user's professional profile
        partner = request.env.user.partner_id
        professional = request.env['proseit.professional'].sudo().search([('partner_id', '=', partner.id)], limit=1)

        if not professional:
            return request.redirect('/my')  # Redirect to portal home if no professional profile

        # Fetch projects associated with the professional
        projects = request.env['proseit.project'].sudo().search([('professional_id', '=', professional.id)])

        return request.render('proseit.portal_my_projects', {
            'projects': projects,
            'page_name': 'projects',
        })

    @http.route(['/my/projects/new'], type='http', auth="user", website=True)
    def new_project(self, **kw):
        return request.render('proseit.portal_new_project', {})

    @http.route(['/my/projects/create'], type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def create_project(self, **post):
        partner = request.env.user.partner_id
        professional = request.env['proseit.professional'].sudo().search([('partner_id', '=', partner.id)], limit=1)

        # Create the new project
        request.env['proseit.project'].sudo().create({
            'title': post.get('title'),
            'sponsorship_type': post.get('sponsorship_type'),
            'project_type': post.get('project_type'),
            'description': post.get('description'),
            'objective': post.get('objective'),
            'visibility': post.get('visibility'),
            'professional_id': professional.id,
        })
        return request.redirect('/my/projects')

    @http.route(['/my/projects/edit/<int:project_id>'], type='http', auth="user", website=True)
    def edit_project(self, project_id, **kw):
        project = request.env['proseit.project'].sudo().browse(project_id)
        return request.render('proseit.portal_edit_project', {
            'project': project
        })

    @http.route(['/my/projects/update/<int:project_id>'], type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def update_project(self, project_id, **post):
        project = request.env['proseit.project'].sudo().browse(project_id)
        if project:
            project.write({
                'title': post.get('title'),
                'sponsorship_type': post.get('sponsorship_type'),
                'project_type': post.get('project_type'),
                'description': post.get('description'),
                'objective': post.get('objective'),
                'visibility': post.get('visibility'),
            })
        return request.redirect('/my/projects')
    
    def _prepare_home_portal_values(self, counters):
        # Call the super method to get the base portal values
        values = super()._prepare_home_portal_values(counters)

        # Find the professional record associated with the current user
        professional = request.env['proseit.professional'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)], limit=1
        )

        # If 'my_projects_count' is a counter, calculate and add the count of the user's projects
        if 'my_projects_count' in counters:
            # Count the number of projects for the professional
            values['my_projects_count'] = 1 if professional else 0
 
        return values

