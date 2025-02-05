from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import ValidationError
import base64
import logging
import json
from datetime import datetime

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
        _logger.info("Received data: %s", post)

        try:
            # Input validation
            if not post.get('name'):
                raise ValidationError(_("Name is required."))
            if not post.get('email'):
                raise ValidationError(_("Email is required."))
            if not post.get('phone'):
                raise ValidationError(_("Phone number is required."))

            # Partner Data
            partner_data = {
                'name': post.get('name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
            }

            # Image Handling for Partner
            if 'professional_photo' in post:
                image = post['professional_photo']
                if image and image.filename and image.content_type.startswith('image/'):
                    partner_data['image_1920'] = base64.b64encode(image.read())
                else:
                    raise ValidationError(_("Invalid image file. Please upload a valid image."))

            new_partner = request.env['res.partner'].sudo().create(partner_data)

            # Professional Profile Data
            professional_data = {
                'name': post.get('name'),
                'date_of_birth': post.get('date_of_birth'),
                'alt_email': post.get('alt_email'),
                'identification_number': post.get('identification_number'),
                'sex': post.get('sex'),
                'years_experience': post.get('years_experience'),
                'work_links': post.get('work_links'),
                'specializations': post.get('specializations'),
                'committee_of_interest': post.get('committee_of_interest'),
                'bank_account': post.get('bank_account'),
                'mobile_money_number': post.get('mobile_money_number'),
                'approval_status': 'pending',
                'partner_id': new_partner.id,
            }

            # Image Handling for Professional Photos
            if 'professional_photos' in post:
                professional_image = post['professional_photos']
                if professional_image and professional_image.filename and professional_image.content_type.startswith('image/'):
                    professional_data['professional_photos'] = base64.b64encode(professional_image.read())
                else:
                    raise ValidationError(_("Invalid professional photo. Please upload a valid image."))

            professional = request.env['proseit.professional'].sudo().create(professional_data)

            # Capture Education Details
            education_entries_json = post.get('education_entries')
            if education_entries_json:
                _logger.info("Received education_entries_json: %s", education_entries_json)
                
                try:
                    education_entries = json.loads(education_entries_json)
                    _logger.info("Parsed education_entries: %s", education_entries)
                    
                    # Group entries by their index
                    grouped_entries = {}
                    for entry_id, value in education_entries.items():
                        # Extract the index number from the key (e.g., "institution_1" -> "1")
                        index = entry_id.split('_')[-1]
                        field_name = '_'.join(entry_id.split('_')[:-1])  # Get the field name without index
                        
                        if index not in grouped_entries:
                            grouped_entries[index] = {}
                        grouped_entries[index][field_name] = value

                    # Process each group of entries
                    for entries in grouped_entries.values():
                        if all(key in entries for key in ['institution', 'level']):
                            try:
                                # Parse dates if they exist
                                start_date = None
                                completion_date = None
                                
                                if 'start_year' in entries:
                                    start_date = datetime.strptime(entries['start_year'], '%Y-%m-%d').date()
                                if 'year' in entries:
                                    completion_date = datetime.strptime(entries['year'], '%Y-%m-%d').date()

                                education_data = {
                                    'institution_name': entries['institution'],
                                    'education_level': entries['level'],
                                    'start_year': start_date,
                                    'completion_year': completion_date,
                                    'professional_id': professional.id,
                                }
                                
                                request.env['proseit.education'].sudo().create(education_data)
                                _logger.info(f"Created education entry: {education_data}")
                                
                            except ValueError as e:
                                _logger.error(f"Date parsing error: {str(e)}")
                            except Exception as e:
                                _logger.error(f"Error creating education entry: {str(e)}")
                        else:
                            _logger.warning(f"Incomplete education entry: {entries}")

                except json.JSONDecodeError as e:
                    _logger.error(f"Failed to parse education_entries_json: {str(e)}")
                except Exception as e:
                    _logger.error(f"Unexpected error processing education entries: {str(e)}")

            # Capture Certification Details
            certification_entries_json = post.get('certification_entries')
            if certification_entries_json:
                _logger.info("Received certification_entries_json: %s", certification_entries_json)

                try:
                    certification_entries = json.loads(certification_entries_json)
                    for entry_id, details in certification_entries.items():
                        if 'name' in details and 'organization' in details:
                            # Check for missing dates
                            date_awarded = details.get('awarded')
                            expiration_date = details.get('expiration')
                            
                            if not date_awarded:
                                _logger.warning(f"Missing awarded date for certification: {details['name']} from {details['organization']}")
                            if not expiration_date:
                                _logger.warning(f"Missing expiration date for certification: {details['name']} from {details['organization']}")

                            certification_data = {
                                'certification_name': details['name'],
                                'issuing_organization': details['organization'],
                                'type_of_certification': details['type'],
                                'date_awarded': date_awarded,
                                'expiration_date': expiration_date,
                                'competency_level': details['competency_level'],
                                'certification_number': details['certification_number'],
                                'professional_id': professional.id,
                            }
                            request.env['proseit.certification'].sudo().create(certification_data)
                        else:
                            _logger.warning(f"Incomplete certification entry: {details}")

                except json.JSONDecodeError as e:
                    _logger.error(f"Failed to parse certification_entries_json: {str(e)}")
                except Exception as e:
                    _logger.error(f"Unexpected error processing certifications: {str(e)}")

            # Process Technical Skills
            technical_skills_json = post.get('technical_skills_entries')
            if technical_skills_json:
                try:
                    technical_skills = json.loads(technical_skills_json)
                    for skill_id, details in technical_skills.items():
                        request.env['proseit.skills'].sudo().create({
                            'skill_name': details['name'],
                            'competency_level': details['competency'],
                            'professional_id': professional.id,
                        })
                except json.JSONDecodeError:
                    _logger.error("Failed to parse technical skills JSON.")

            # Process Soft Skills
            soft_skills_json = post.get('soft_skills_entries')
            if soft_skills_json:
                try:
                    soft_skills = json.loads(soft_skills_json)
                    for skill_id, details in soft_skills.items():
                        request.env['proseit.soft_skills'].sudo().create({
                            'skill_name': details['name'],
                            'competency_level': details['competency'],
                            'professional_id': professional.id,
                        })
                except json.JSONDecodeError:
                    _logger.error("Failed to parse soft skills JSON.")

            return request.redirect('/professional/thankyou')

        except ValidationError as e:
            return request.render("proseit.portal_professional_registration", {
                'error_message': str(e),
                'page_name': 'professional_registration',
            })
    
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