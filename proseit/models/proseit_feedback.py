from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProseitFeedback(models.Model):
    _name = 'proseit.feedback'
    _description = 'Professional Feedback'
    
    # Reference to the res.partner (via proseit.client)
    client_id = fields.Many2one('res.partner', ondelete='cascade', string='Client', required=True)

    description = fields.Text(string='Feedback Description')
    nda = fields.Boolean(string='NDA Signed')
    public_profile = fields.Boolean(string='Public Profile')

    # Reference to the professional
    professional_id = fields.Many2one('proseit.professional', string='Professional', ondelete='cascade', required=True)

    feedback = fields.Text(string='Feedback')
    date_provided = fields.Date('Date Provided', default=fields.Date.today)
    
    rating = fields.Selection([
        ('1', '1 - Poor'),
        ('2', '2 - Fair'),
        ('3', '3 - Good'),
        ('4', '4 - Very Good'),
        ('5', '5 - Excellent')
    ], string='Rating', required=True)

    # Validation to ensure that feedback text is provided for ratings below a certain threshold
    @api.constrains('rating', 'feedback_text')
    def _check_feedback_text(self):
        for record in self:
            if record.rating in ['1', '2'] and not record.feedback_text:
                raise ValidationError('Feedback text is required for ratings below 3.')

    # Override name_get to display client and professional names in feedback records
    def name_get(self):
        result = []
        for feedback in self:
            name = f"Feedback from {feedback.client_id.name} on {feedback.professional_id.name}"
            result.append((feedback.id, name))
        return result
