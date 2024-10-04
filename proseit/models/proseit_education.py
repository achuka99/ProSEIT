from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProseitEducation(models.Model):
    _name = 'proseit.education'
    _description = 'Education Details'

    # Inheriting from res.partner for contact functionality
    professional_id = fields.Many2one('proseit.professional', ondelete='cascade', string='Professional', required=True)

    # Education Details
    institution_name = fields.Char(required=True, string='Institution Name')
    education_level = fields.Selection([
        ('a_level', 'A-Level'), 
        ('o_level', 'O-Level'), 
        ('university', 'University/Tertiary')
    ], required=True, string='Education Level')
    
    completion_year = fields.Char(required=True, string='Year of Completion')

    # Override name_get to display the institution name
    def name_get(self):
        result = []
        for education in self:
            name = f"{education.institution_name} ({education.education_level})"
            result.append((education.id, name))
        return result
