from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartners(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('odoo', 'Hospital')])
    # Override create function in odoo
    @api.model
    def create(self, vals):
        res = super(ResPartners, self).create(vals)
        # custom coding here
        return res


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    patient_name = fields.Char(string='Patient Name')
    is_patient = fields.Boolean(string='Is Patient')
    def action_confirm(self):
        res = super(SaleOrderInherit, self).action_confirm()
        print("Hello odoo")
        return res


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'
    _rec_name = 'patient_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def print_report_excel(self):
        return self.env.ref('odoo_hospital.report_patient_card_xlx').report_action(self)

    def print_report(self):
        return self.env.ref('odoo_hospital.report_patient_card').with_context({'discard_logo_check': True}).report_action(self)
    #Odoo ORM
    def test_recordset(self):
        partners = self.env['res.partner'].search([])
        print('Mapped Partners', partners.mapped('email'))
        print('Sorted partners', partners.sorted(lambda o: o.write_date, reverse=True))
        print('Filtered partners', partners.filtered(lambda o: o.parent_id))

    def action_patients(self):
        print('Hello action patients working!')
        return {
            'name': ('Patient Server Action'),
            'domain': [],
            'view_type': 'form',
            'res_model': 'hospital.patient',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
    @api.model
    def test_cron_job(self):
        print('Hello')

    def name_get(self):
        res = []
        for field in self:
            res.append((field.id, '%s %s' % (field.name_seq, field.patient_name)))
        return res

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        domain = args + ['|', ('name_seq', operator, name), ('patient_name', operator, name)]
        return super(HospitalPatient, self).search(domain, limit=limit).name_get()

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError('The age must be greater then 5')

    def _get_default_notes(self):
        return 'This is a normal problem!'

    def open_patient_appointments(self):
        return {
            'name': ('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    @api.model
    def create(self, vals):
        if vals.get('name_seq', ('New')) == ('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or ('New')
        result = super(HospitalPatient, self).create(vals)
        return result

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            # if rec.patient_age:
            if rec.patient_age < 18:
                rec.age_group = 'minor'
            else:
                rec.age_group = 'major'

    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count

    def action_send_card(self):
        template_id = self.env.ref('odoo_hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    patient_name = fields.Char(string='Name', required=True, track_visibility='always')

    name_seq = fields.Char(string='Patient ID', required=True, copy=False, readonly=True, index=True,
                           default=lambda self: ('New'))
    patient_age = fields.Integer(string='Age', track_visibility='always', group_operator=False)
    patient_age2 = fields.Float(string='Age 2')
    patient_name_upper = fields.Char(compute='_compute_upper_name', inverse='_inverse_upper_name')
    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False

    @api.depends('patient_name')
    def _inverse_upper_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name else False
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male', string='Gender')

    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),
    ], string='Age Group', compute='set_age_group', store=True)

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    doctor_gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male', string='Doctor Gender')

    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender

    doctor_ids = fields.Many2many('hospital.doctor', string='Visitor Doctors list')
    blood_group = fields.Char(string='Blood Group')
    notes = fields.Text(string='Notes', default=_get_default_notes)
    image = fields.Binary(string='Image')
    active = fields.Boolean('Active', default=True)
    appointment_count = fields.Integer(string='Appointment', compute="get_appointment_count")
    email_id = fields.Char(string='Email')
    contact_no = fields.Char(string="Contact No.")
    user_id = fields.Many2one('res.users', string='PRO')
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.user.company_id)
