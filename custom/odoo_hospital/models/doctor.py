from odoo import models, fields, api


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor Record'
    _rec_name = 'doctor_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def create(self, vals):
        if vals.get('doc_seq', ('New')) == ('New'):
            vals['doc_seq'] = self.env['ir.sequence'].next_by_code('hospital.doctor.sequence') or ('New')
        result = super(HospitalDoctor, self).create(vals)
        return result

    doc_seq = fields.Char(string='Doctor Sequence', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    # doctor_id = fields.Many2one('res.users', string='Doctor', required=True)
    doctor_id = fields.Char(string='Doctor Name')
    speciality = fields.Text('Speciality')
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male', string='Gender')