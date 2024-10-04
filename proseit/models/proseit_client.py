from odoo import models, fields

class ProseitClient(models.Model):
    _name = 'proseit.client'
    _description = 'ProSEIT Client Profile'
    _inherits = {'res.partner': 'partner_id'}  # Using delegation inheritance
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # Link to the res.partner model
    partner_id = fields.Many2one('res.partner', ondelete="cascade", required=True)

    # Basic Information (Inherited res.partner has fields like name, phone, and email)
    password = fields.Char(string="Password", required=True)
    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Sex", required=True)

    # Preferences
    specialization_ids = fields.Many2many('proseit.specialization', string="Professional Specializations")

    # Feedback
    feedback_ids = fields.One2many('proseit.feedback', 'client_id', string="Feedback")
    client_id = fields.Char('Client ID', readonly=True)

    # Tagging clients for differentiation
    category_id = fields.Many2many(
        'res.partner.category', 
        string='Tags', 
        default=lambda self: self.env.ref('proseit.client_tag').ids  # Assigning default client tag
    )

    # Override name_get to display first name and surname instead of the full name
    def name_get(self):
        result = []
        for client in self:
            name = f"{client.first_name} {client.surname}"
            result.append((client.id, name))
        return result
