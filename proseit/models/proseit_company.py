from odoo import models, fields

class ProseitCompany(models.Model):
    _name = 'proseit.company'  # Define the model name
    _description = 'ProSEIT Company/Startup Profile'
    _inherits = {'res.partner': 'partner_id'}  # Using delegation inheritance
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # Link to the res.partner model
    partner_id = fields.Many2one('res.partner', ondelete="cascade", required=True)

    # Contact Information (res.partner already contains fields like name, phone, and email)
    company_name = fields.Char(string="Company Name", required=True)

    # Company/Startup Details
    business_description = fields.Text('Business Description', required=True)
    business_stage = fields.Selection([
        ('startup', 'Startup'), 
        ('sme', 'SME'), 
        ('enterprise', 'Enterprise')
    ], string='Business Stage', required=True)
    business_photos = fields.Binary('Business Photos')
    business_website = fields.Char('Business Website')
    looking_for_investment = fields.Boolean('Looking for Investment?')
    public_profile = fields.Boolean('Public Profile for Investors', default=False)
    
    # Related Fields
    testimonials_ids = fields.One2many('proseit.company.testimonial', 'company_id', string="Company Testimonials")

    # Tagging companies for differentiation
    category_id = fields.Many2many(
        'res.partner.category', 
        string='Tags', 
        default=lambda self: self.env.ref('proseit.company_tag').ids  # Assigning default company tag
    )

    # Override name_get to display the company name
    def name_get(self):
        result = []
        for company in self:
            name = company.company_name
            result.append((company.id, name))
        return result
