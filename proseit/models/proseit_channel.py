from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProseitChannel(models.Model):
    _name = 'proseit.channel'
    _description = 'Channel for Professionals'

    name = fields.Char(string="Channel Name", required=True)
    professional_ids = fields.Many2many('proseit.professional', string='Professionals')
