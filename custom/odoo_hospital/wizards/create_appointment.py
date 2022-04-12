from odoo import models, fields


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')

    appointment_date = fields.Date(string='Appointment Date')

    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'doctor_id': self.doctor_id.id,
            'appointment_date': self.appointment_date,
        }
        self.env['hospital.appointment'].create(vals)