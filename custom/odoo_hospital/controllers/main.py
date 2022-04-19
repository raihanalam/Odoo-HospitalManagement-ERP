from odoo import http
from odoo.http import request

class HospitalDoctor(http.Controller):
    @http.route('/hospital/patient/', website=True, auth='public')
    def hospital_patient(selfself, **kw):
        patients = request.env['hospital.patient'].sudo().search([])
        return request.render("odoo_hospital.patients_page", {'patients':patients})