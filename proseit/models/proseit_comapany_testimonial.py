from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProseitCompanyTestimonial(models.Model):
    _name = 'proseit.company.testimonial'
    _description = 'Company Testimonials'

    # Related Company
    company_id = fields.Many2one('proseit.company', ondelete='cascade', string='Company', required=True)

    # Client Information
    client_id = fields.Many2one('proseit.client', ondelete='set null', string='Client', help="The client providing the testimonial")

    # Testimonial Information
    feedback = fields.Text('Feedback', required=True)
    project_description = fields.Text('Project Description', help="Description of the project the testimonial refers to")
    completion_year = fields.Integer('Year of Completion', help="Year when the project was completed")

    # Validations
    @api.constrains('completion_year')
    def _check_completion_year(self):
        for record in self:
            if record.completion_year and record.completion_year > fields.Date.today().year:
                raise ValidationError('The year of completion cannot be in the future.')
