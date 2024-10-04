from odoo import models, fields

class ProseitSkills(models.Model):
    _name = 'proseit.skills'
    _description = 'Technical Skills'

    professional_id = fields.Many2one('proseit.professional', ondelete='cascade', string='Professional')  # Link to res.partner
    skill_name = fields.Char(string="Technical Skill", required=True)
    competency_level = fields.Selection([
        ('1', '1 - Beginner'),
        ('2', '2 - Novice'),
        ('3', '3 - Competent'),
        ('4', '4 - Proficient'),
        ('5', '5 - Expert')
    ], string="Competency Level", required=True)
