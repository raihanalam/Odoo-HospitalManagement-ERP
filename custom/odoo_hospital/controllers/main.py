from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
class AppointmentController(http.Controller):
    @http.route('/odoo_hospital/appointments', auth='user', type='json')
    def appointment_banner(self):
        return {
            'html': """<div style="padding:50px;">
                        <link>
                        <center><h3>
                        <font color="red">
                        Hello I'm Raihan Alam and I'm learning Odoo ERP Software Development</font>
                        </h3></center>
                        </div>"""
        }

class WebsiteSaleInherit(WebsiteSale):
    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        res = super(WebsiteSaleInherit, self).shop(page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post)
        print("Inherited odoo dev", res.qcontext.update({'search': 'hello odoo'}))
        return res

class Hospital(http.Controller):
    @http.route('/patient_webform', type='http', auth='public', website=True)
    def patient_webform(self, **kwargs):
        doc_rec = request.env['hospital.doctor'].sudo().search([])
        return http.request.render('odoo_hospital.create_patient', {'doctor_rec': doc_rec})

    @http.route('/create/webpatient', type='http', auth='public', website=True)
    def create_webpatient(self, **kwargs):
        request.env['hospital.patient'].sudo().create(kwargs)
        # doc = {
        #     'doctor_id': kwargs.get('patient_name')
        # }
        # request.env['hospital.doctor'].sudo().create(doc)
        return http.request.render('odoo_hospital.patient_thanks', {})

    @http.route('/hospital/patient/', website=True, auth='public')
    def hospital_patient(self, **kw):
        patients = request.env['hospital.patient'].sudo().search([])
        return request.render("odoo_hospital.patients_page", {'patients': patients})

    @http.route('/create_patient', type='json', auth='user')
    def create_patient(self, **rec):
        if request.jsonrequest:
            if rec['name']:
                vals = {
                    'patient_name': rec['name'],
                    'email_id': rec['email']
                }
                new_patient = request.env['hospital.patient'].sudo().create(vals)
                args = {'success': True, 'message': 'Success', 'ID': new_patient.id}
        return args

    @http.route('/get_patient', type='json', auth='user')
    def get_patient(self):
        patients_rec = request.env['hospital.patient'].search([])
        patients = []
        for rec in patients_rec:
            vals = {
                'id': rec.id,
                'name': rec.patient_name,
                'sequence': rec.name_seq
            }
            patients.append(vals)
        print(patients)
        data = {'status': 200, 'response': patients, 'message': 'Success'}
        return data

    @http.route('/update_patient', type='json', auth='user')
    def update_patient(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                patient = request.env['hospital.patient'].sudo().search([('id', '=', rec['id'])])
                if patient:
                    patient.sudo().write(rec)
                args = {'success': True, 'message': 'Success'}
        return args
