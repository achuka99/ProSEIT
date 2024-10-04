from odoo import models, fields

class ProseitTestimonial(models.Model):
    _name = 'proseit.testimonial'
    _description = 'Professional Testimonials'

    description = fields.Text('Brief Details', required=True)
    nda = fields.Boolean('Work done under NDA?')
    public_profile = fields.Boolean('Show in Public Profile?')
    reference_contact = fields.Char('Reference Contact (Email/Phone)', required=True)
    certified_by_proseit = fields.Boolean('Certified by ProSEIT?')
    proficiency = fields.Selection(
        [('1', '1 - Novice'), 
         ('2', '2 - Intermediate'), 
         ('3', '3 - Proficient'), 
         ('4', '4 - Advanced'), 
         ('5', '5 - Expert')],
        string="Proficiency of Execution", required=True)
    collaboration_members = fields.Text('Collaboration Members (Phone/Email)')
    supporting_documents = fields.Many2many('ir.attachment', string="Supporting Documents")
    verifiable = fields.Selection([('verifiable', 'Verifiable'), ('not_verifiable', 'Not Verifiable')], 
                                  string="Verifiability", required=True)
    
    professional_id = fields.Many2one('proseit.professional', ondelete='cascade', string="Professional")
