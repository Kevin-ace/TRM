from odoo import models, fields, api


class TritelRequest(models.Model):
    _name = 'tritel.request'
    _description = 'Tritel Request'

    name = fields.Char(string='Request Description', required=True)
    amount_ksh = fields.Monetary(string='Amount (KSH)', currency_field='currency_id', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.ref('base.KES').id,
                                  required=True)
    request_date = fields.Datetime(string='Request Date')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
    ], string='Status', default='draft', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('reviewed', 'Reviewed'),
    ], string='Status', default='draft', readonly=True)

    @api.model
    def create(self, vals):
        if 'status' not in vals:
            vals['status'] = 'draft'
        return super(TritelRequest, self).create(vals)

    def write(self, vals):
        if 'name' in vals or 'amount_ksh' in vals or 'request_date' in vals:
            name = vals.get('name', self.name)
            amount_ksh = vals.get('amount_ksh', self.amount_ksh)
            request_date = vals.get('request_date', self.request_date)
            if name and amount_ksh and request_date:
                vals['status'] = 'submitted'
        return super(TritelRequest, self).write(vals)
