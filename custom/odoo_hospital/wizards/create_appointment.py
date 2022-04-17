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
        self.patient_id.message_post(body='Appointment Created Successfully', subject="Appointment")

    def get_data(self):
        appointments = self.env['hospital.appointment'].search([('patient_id', '=', 6)]) #search_count is for counting data
        for rec in appointments:
            print('Appointment Name', rec.name)
        # return {
        #     "type": "ir.actions.do_nothing"
        # }

    def delete_patient(self):
        for rec in self:
            rec.patient_id.unlink()
