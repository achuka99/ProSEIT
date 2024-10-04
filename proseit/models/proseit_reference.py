from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProseitReference(models.Model):
    _name = 'proseit.references'
    _description = 'Verification References'

    # Reference to the testimonial
    testimonial_id = fields.Many2one('proseit.testimonial', ondelete='cascade', string='Testimonial')

    # Reference Name (can be derived from the contact_id)
    name = fields.Char(string='Reference Name', required=True)
    
    # Contact Details field, can also be derived from the contact_id
    contact = fields.Char(string='Contact Details (Phone or Email)', required=True)

    @api.constrains('contact')
    def _check_contact(self):
        for record in self:
            if not record.contact:
                raise ValidationError('Contact details must be provided.')

    @api.onchange('contact_id')
    def _onchange_contact_id(self):
        if self.contact_id:
            self.name = self.contact_id.name
            self.contact = self.contact_id.phone or self.contact_id.email or 'No contact details available'
        else:
            self.name = ''
            self.contact = ''

    # Override name_get to display reference name
    def name_get(self):
        result = []
        for reference in self:
            name = reference.name or "Unnamed Reference"
            result.append((reference.id, name))
        return result
