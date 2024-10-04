from odoo import models, fields, api

class ProSEITJobPosting(models.Model):
    _name = 'proseit.job.posting'
    _description = 'Job Posting'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Inherit the mail thread and activity mixins

    title = fields.Char(string='Job Title', required=True)
    description = fields.Text(string='Job Description', required=True)
    requirements = fields.Text(string='Job Requirements', required=True)
    salary = fields.Char(string='Salary')
    location = fields.Char(string='Location')
    
    # Reference to either a client or company
    client_id = fields.Many2one('proseit.client', string='Posted by Client')
    company_id = fields.Many2one('proseit.company', string='Posted by Company')

    application_deadline = fields.Date(string='Application Deadline')
    
    # Approval status (pending, approved, rejected)
    approval_status = fields.Selection([('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', string='Approval Status', tracking=True)
    
    # Job posting by either client or company
    def name_get(self):
        result = []
        for job in self:
            if job.client_id:
                name = f"{job.title} (Posted by {job.client_id.name})"
            elif job.company_id:
                name = f"{job.title} (Posted by {job.company_id.company_name})"
            else:
                name = job.title
            result.append((job.id, name))
        return result

    # Example method to approve the job posting
    def approve_job(self):
        self.approval_status = 'approved'
        self.message_post(body="The job posting has been approved.")

    # Example method to reject the job posting
    def reject_job(self):
        self.approval_status = 'rejected'
        self.message_post(body="The job posting has been rejected.")

    # Optional: Method to reset approval status to pending
    def reset_to_pending(self):
        self.approval_status = 'pending'
        self.message_post(body="The job posting approval status has been reset to pending.")

    # Ensure one of these is always set
    # _sql_constraints = [
    #     ('client_or_company', 'CHECK(client_id IS NOT NULL OR company_id IS NOT NULL)', 'Job posting must be linked to either a client or a company.')
    # ]
