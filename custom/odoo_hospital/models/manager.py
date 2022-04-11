from odoo import models, fields, api

class HospitalManager(models.Model):
    _name = 'hospital.manager'
    _description = 'Manager Record'
    _rec_name = 'manager_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def create(self, vals):
        if vals.get('man_seq', ('New')) == ('New'):
            vals['man_seq'] = self.env['ir.sequence'].next_by_code('hospital.manager.sequence') or ('New')
        result = super(HospitalManager, self).create(vals)
        return result

    man_seq = fields.Char(string='Manager Sequence', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    manager_id = fields.Many2one('res.users', string='Manager', required=True)
    designation = fields.Text('Designation')
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male', string='Gender')