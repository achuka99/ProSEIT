from odoo import models, fields

class ProseitSoftSkills(models.Model):
    _name = 'proseit.soft_skills'
    _description = 'Soft Skills'

    professional_id = fields.Many2one('proseit.professional', ondelete='cascade', string='Professional')  # Reference to res.partner
    skill_name = fields.Char('Soft Skill', required=True)
    competency_level = fields.Selection([
        ('1', '1 - Beginner'),
        ('2', '2 - Novice'),
        ('3', '3 - Competent'),
        ('4', '4 - Proficient'),
        ('5', '5 - Expert')
    ], string="Competency Level", required=True)
