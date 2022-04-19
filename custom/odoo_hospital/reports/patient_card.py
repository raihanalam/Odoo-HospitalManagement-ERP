from odoo import models, api


class PatientCardReport(models.AbstractModel):
    _name = 'report.odoo_hospital.report_patient'
    _description = 'Patient Card Report'

    @api.model
    def _get_report_values(self, docids, data=None):

        docs = self.env['hospital.patient'].browse(docids[0])
        appointments = self.env['hospital.appointment'].search([('patient_id', '=', docids[0])])
        # limit=1 we can also set limit
        appointment_list = []

        for app in appointments:
            vals = {
                'name': app.name,
                'notes': app.notes,
                'appointment_date': app.appointment_date
            }
            appointment_list.append(vals)
        # print(appointment_list)
        return {
            'doc_model': 'hospital.patient',
            'data': data,
            'docs': docs,
            'appointment_list': appointment_list
        }