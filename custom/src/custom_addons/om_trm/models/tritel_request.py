from odoo import models, fields, api


class TritelRequest(models.Model):
    _name = 'tritel.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Tritel Request'

    name = fields.Char(string='Request Description')
    amount_ksh = fields.Monetary(string='Amount (KSH)', currency_field='currency_id', required=True)
    # state = fields.Selection([('draft', 'Draft'), ('in_progress', 'In Progress'), ('done', 'Done')], string='State')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.ref('base.KES').id,
                                  required=True)
    request_date = fields.Datetime(string='Request Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('reviewed', 'Reviewed'),
        ('archived', 'Archived'),
    ], string='State', default='draft', readonly=True, required=True, track_visibility='onchange')
    #
    # def state_color(self, state_value):
    #     state_colors = {
    #         'draft': '#ff9800',  # Orange
    #         'approve': '#4caf50',  # Green
    #         'cancel': '#f44336',  # Red
    #     }
    #     return state_colors.get(state_value, '#9e9e9e')  # Default to gray

    archived_count = fields.Integer(compute='_compute_archived_count', string="Archived Count")


    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_reviewed(self):
        self.write({'state': 'reviewed'})

    def action_archived(self):
        self.write({'state': 'archived'})

    @api.model
    def create(self, vals):
        if 'status' not in vals:
            vals['state'] = 'draft'
        return super(TritelRequest, self).create(vals)

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'reviewed':
            vals['state'] = 'archived'
        if 'name' in vals or 'amount_ksh' in vals or 'request_date' in vals:
            name = vals.get('name', self.name)
            amount_ksh = vals.get('amount_ksh', self.amount_ksh)
            request_date = vals.get('request_date', self.request_date)
            if name and amount_ksh and request_date:
                vals['state'] = 'submitted'
        return super(TritelRequest, self).write(vals)

    @api.depends('state')
    def _compute_archived_count(self):
        for record in self:
            record.archived_count = self.search_count([('state', '=', 'archived')])

    def action_get_archived_records(self):
        return {
            'name': 'Archived Requests',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'tritel.request',
            'domain': [('state', '=', 'archived')],
            'context': dict(self.env.context),
        }


show_submit = fields.Boolean(compute='_compute_show_submit')


@api.depends('state')
def _compute_show_submit(self):
    for record in self:
        record.show_submit = record.state == 'draft'

        # show_submit = fields.Boolean(compute='_compute_show_submit')
# @api.depends('state')
# def _compute_show_submit(self):
#     for record in self:
#         record.show_submit = record.state == 'draft'
