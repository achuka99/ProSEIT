from odoo import models, fields

class ProseitCertification(models.Model):
    _name = 'proseit.certification'
    _description = 'Professional Certification'

    professional_id = fields.Many2one('proseit.professional', ondelete='cascade', string='Professional')
    certification_name = fields.Char('Certification Name', required=True)
    issuing_organization = fields.Char('Issuing Organization', required=True)
    date_awarded = fields.Date('Date Awarded')
    expiration_date = fields.Date('Expiration Date')

    # Binary field for the certificate document (image/pdf)
    certificate_document = fields.Binary('Certificate Document')
    certificate_filename = fields.Char('Certificate Filename')  # To store the filename for downloads
