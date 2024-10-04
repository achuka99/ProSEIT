from odoo import models, fields, api

class ProSEITProject(models.Model):
    _name = 'proseit.project'
    _description = 'ProSEIT Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Inherit the mail thread and activity mixins

    title = fields.Char(string='Project Title', required=True)
    sponsorship_type = fields.Selection([
        ('funded', 'Funded'),
        ('open_source', 'Open Source'),
        ('csr', 'Corporate Social Responsibility (CSR)'),
    ], string='Sponsorship Type', required=True)
    project_type = fields.Selection([
        ('public', 'Public'),
        ('private', 'Private'),
    ], string='Project Type', required=True)
    description = fields.Text(string='Project Description', help='Brief description of the project (300 words max)')
    objective = fields.Text(string='Main Objective')
    visibility = fields.Selection([
        ('portal', 'Visible on ProSEIT Portal'),
        ('public', 'Visible on Public Profile'),
        ('private', 'Private'),
    ], string='Visibility', default='portal')
    professional_id = fields.Many2one('proseit.professional', string='Professional', required=True)
    collaborator_ids = fields.Many2many('proseit.professional', string='Collaborators')
