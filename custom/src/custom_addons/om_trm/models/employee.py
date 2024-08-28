from odoo import models, fields


class TritelEmployee(models.Model):
    _name = 'tritel.employee'
    _description = 'Tritel Employee'

    # Your model fields and methods here
    name = fields.Char(string='Name', required=True)
    job_title = fields.Char(string='Job Title')
    department_id = fields.Many2one('hr.department', string='Department')
