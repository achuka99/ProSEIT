from odoo import models, fields, api

class ProseitProfessional(models.Model):
    _name = 'proseit.professional'
    _description = 'ProSEIT Professional Profile'
    _inherits = {'res.partner': 'partner_id'}  # Delegation inheritance
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # Step 1: Bio Info (res.partner already has some fields like name, phone, email)
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    alt_email = fields.Char(string="Alternative Email")
    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], required=True)
    identification_number = fields.Char('NIN/Passport Number', required=True)

    # Linking to res.partner using delegation inheritance
    partner_id = fields.Many2one('res.partner', ondelete="cascade", required=True)

    # Step 2: Professional Details
    education_ids = fields.One2many('proseit.education', 'professional_id', string="Education Details")
    certifications_ids = fields.One2many('proseit.certification', 'professional_id', string="Professional Certifications")
    professional_photos = fields.Binary('Professional Photos', required=True)
    work_links = fields.Text('Links to Professional Work')
    specializations = fields.Text('Professional specializations')
    committee_of_interest = fields.Selection(
        [('software', 'Software Engineers'), 
         ('process', 'Process Analysts'), 
         ('architects', 'Architects')],
         string='Committee of Interest'
    )
    years_experience = fields.Integer('Years of Professional Experience', required=True)

    # Step 3: Skills Map
    technical_skills = fields.One2many('proseit.skills', 'professional_id', string="Technical Skills")
    soft_skills = fields.One2many('proseit.soft_skills', 'professional_id', string="Soft Skills")
    testimonials = fields.One2many('proseit.testimonial', 'professional_id', string="Work Testimonials")
    supporting_documents = fields.Many2many('ir.attachment', string="Supporting Documents")

    # Step 4: Financial Account Details
    bank_account = fields.Char('Bank Account Number')
    mobile_money_number = fields.Char('Mobile Money Number')
    alternative_payment_channels = fields.Selection(
        [('springpesa', 'SpringPesa'), 
         ('xente', 'Xente')], 
        string='Alternative Payment Channels'
    )

    # Step 5: Approval of Professional Profile
    approval_status = fields.Selection([('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', string='Status', tracking=True)
    professional_id = fields.Char('Professional ID', readonly=True)

    feedback_ids = fields.One2many('proseit.feedback', 'professional_id', string="Feedback")
    linkedin_profile = fields.Char('LinkedIn Profile')

    project_ids = fields.One2many('proseit.project', 'professional_id', string='Ongoing Projects')

    @api.model
    def approval_status_groups(self, present_ids, domain, **kwargs):
        status_values = self.env['proseit.professional'].fields_get(all=['approval_status'])['approval_status']['selection']
        folded = {status: True for status in ['pending', 'approved', 'rejected']}
        return status_values, folded

    _group_by_full = {
        'approval_status': approval_status_groups,
    }

    # Example method to approve the professional profile
    def approve_profile(self):
        self.approval_status = 'approved'
        self.message_post(body="The professional profile has been approved.")

    # Example method to reject the professional profile
    def reject_profile(self):
        self.approval_status = 'rejected'
        self.message_post(body="The professional profile has been rejected.")
        
    # Optional: Method to reset approval status to pending
    def reset_to_pending(self):
        self.approval_status = 'pending'
        self.message_post(body="The professional profile status has been reset to pending.")
