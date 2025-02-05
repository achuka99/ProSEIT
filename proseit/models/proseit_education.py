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
        ('o_level', 'O-Level'),
        ('gcse', 'GCSE'),
        ('gse', 'GSE'),
        ('a_level', 'A-Level'),
        ('ordinary_certificate', 'Ordinary Certificate'),
        ('ordinary_diploma', 'Ordinary Diploma'),
        ('bachelors', 'Bachelors Degree'),
        ('masters', 'Masters Degree'),
        ('phd', 'PhD'),
        ('others', 'Others')
    ], required=True, string='Education Level')

    start_year = fields.Date(required=True, string='Start Date')
    
    completion_year = fields.Date(required=True, string='Completion Date')

    # Override name_get to display the institution name
    def name_get(self):
        result = []
        for education in self:
            name = f"{education.institution_name} ({education.education_level})"
            result.append((education.id, name))
        return result
