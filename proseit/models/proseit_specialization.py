from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProseitSpecialization(models.Model):
    _name = 'proseit.specialization'
    _description = 'Professional Specializations'

    name = fields.Char(string='Specialization Name', required=True)

    # Description of the specialization
    description = fields.Text(string='Description')

    # Related professionals (using res.partner)
    professional_ids = fields.Many2many('proseit.professional', string='Professionals', 
                                         help='Contacts associated with this specialization')

    # Tagging for easier categorization
    category_id = fields.Many2many(
        'res.partner.category', 
        string='Tags', 
        help='Tags for categorizing specializations'
    )

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name:
                raise ValidationError('Specialization name must be provided.')

    def name_get(self):
        result = []
        for specialization in self:
            name = specialization.name
            result.append((specialization.id, name))
        return result
