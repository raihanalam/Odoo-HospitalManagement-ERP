from odoo import models, fields, api


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

    def print_report(self):
        data = {
            'model': 'create.appointment',
            'form': self.read()[0]
        }
        # if data['form']['patient_id']:
        #     selected_patient = data['form']['patient_id'][0]
        #     appointments = self.env['hospital.appointment'].search([('patient_id', '=', selected_patient)])
        # else:
        #     appointments = self.env['hospital.appointment'].search([])
        # appointment_list = []
        # for app in appointments:
        #     vals = {
        #         'name': app.name,
        #         'notes': app.notes,
        #         'appointment_date': appointment_list
        #     }
        #     appointment_list.append(vals)
        # data['appointments'] = appointment_list

        #.with_context({'discard_logo_check': True})
        return self.env.ref('odoo_hospital.report_appointment').report_action(self, data=data)