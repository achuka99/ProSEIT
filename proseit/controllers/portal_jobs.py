from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class PortalJobs(CustomerPortal):

    @http.route(['/my/jobs'], type='http', auth="user", website=True)
    def my_jobs(self, **kw):
        # Get the logged-in user's professional profile
        partner = request.env.user.partner_id
        professional = request.env['proseit.professional'].sudo().search([('partner_id', '=', partner.id)], limit=1)

        if not professional:
            return request.redirect('/my')  # Redirect to portal home if no professional profile

        # Fetch job postings associated with the professional's company or client
        jobs = request.env['proseit.job.posting'].sudo().search([])

        return request.render('proseit.portal_my_jobs', {
            'jobs': jobs,
            'page_name': 'jobs',
        })
    
    def _prepare_home_portal_values(self, counters):
        # Call the super method to get the base portal values
        values = super()._prepare_home_portal_values(counters)

        # Find the professional record associated with the current user
        professional = request.env['proseit.professional'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)], limit=1
        )

        # If 'my_jobs_count' is a counter, calculate and add the count of the user's projects
        if 'my_jobs_count' in counters:
            # Count the number of projects for the professional
            values['my_jobs_count'] = 1 if professional else 0
 
        return values

