from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import logging

_logger = logging.getLogger(__name__)

class PortalProfessional(CustomerPortal):

    @http.route(['/my/professional'], type='http', auth="user", website=True)
    def my_professional_profile(self, **kw):
        # Get the logged-in user's professional profile
        partner = request.env.user.partner_id
        professional = request.env['proseit.professional'].sudo().search([('partner_id', '=', partner.id)], limit=1)

        if not professional:
            return request.redirect('/my')  # Redirect to portal home if no professional profile

        return request.render('proseit.portal_my_professional_profile', {
            'professional': professional,
            'page_name': 'professional',
        })

    @http.route(['/my/professional/update'], type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def update_professional_profile(self, **post):
        # Fetch the logged-in user's professional profile
        partner = request.env.user.partner_id
        professional = request.env['proseit.professional'].sudo().search([('partner_id', '=', partner.id)], limit=1)

        if professional:
            # Update fields with form data
            professional.sudo().write({
                'date_of_birth': post.get('date_of_birth'),
                'alt_email': post.get('alt_email'),
                'sex': post.get('sex'),
                'identification_number': post.get('identification_number'),
                'years_experience': post.get('years_experience'),
                'committee_of_interest': post.get('committee_of_interest'),
                'bank_account': post.get('bank_account'),
                'mobile_money_number': post.get('mobile_money_number'),
                # Update professional photos if a new file is uploaded
                'professional_photos': post.get('professional_photos') and post.get('professional_photos').read(),
            })

        return request.redirect('/my/professional')  # Redirect back to profile after update


    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        # Find the professional record associated with the current user
        professional = request.env['proseit.professional'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)], limit=1
        )

        # Set the count of professionals to 1 if a professional profile exists
        if 'my_professionals_count' in counters:
            values['my_professionals_count'] = 1 if professional else 0
            _logger.info(f'My Professionals Count: {values["my_professionals_count"]}')

        return values
    
    @http.route(['/professional/register'], type='http', auth="public", website=True, csrf=False)
    def professional_registration(self, **kw):
        # Render the registration form
        return request.render('proseit.portal_professional_registration')


    @http.route(['/professional/register/submit'], type='http', methods=['POST'], auth="public", website=True, csrf=False)
    def professional_registration_submit(self, **post):
        # Handle form submission and create a new partner and professional profile

        # Create a new partner (linked to the professional)
        partner_data = {
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
        }
        new_partner = request.env['res.partner'].sudo().create(partner_data)

        # Create a new professional profile linked to the new partner
        professional_data = {
            'name': post.get('name'),
            'date_of_birth': post.get('date_of_birth'),
            'alt_email': post.get('alt_email'),
            'identification_number': post.get('identification_number'),
            'sex': post.get('sex'),
            'years_experience': post.get('years_experience'),
            'committee_of_interest': post.get('committee_of_interest'),
            'bank_account': post.get('bank_account'),
            'mobile_money_number': post.get('mobile_money_number'),
            'professional_photos': post.get('professional_photos'),
            'approval_status': 'pending',  # Set the status to Pending
            'partner_id': new_partner.id,  # Link to the newly created partner
        }

        professional = request.env['proseit.professional'].sudo().create(professional_data)

        # Redirect to a 'thank you' page after successful registration
        return request.redirect('/professional/thankyou')

    
    @http.route(['/professional/thankyou'], type='http', auth="public", website=True)
    def professional_thankyou(self, **kw):
        # Render the thank you page after registration
        return request.render('proseit.portal_professional_thankyou')

    @http.route(['/professional/status'], type='http', auth="user", website=True)
    def professional_status(self, **kw):
        # Fetch the logged-in user's professional profile
        partner = request.env.user.partner_id
        professional = request.env['proseit.professional'].sudo().search([('partner_id', '=', partner.id)], limit=1)

        if not professional:
            return request.redirect('/my')  # Redirect to portal home if no professional profile

        return request.render('proseit.portal_professional_status', {
            'professional': professional,
            'approval_status': professional.approval_status,
        })
