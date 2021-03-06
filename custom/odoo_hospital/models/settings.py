from odoo import models, fields, api
from ast import literal_eval
class HospitalSettings(models.TransientModel):
    #_name = 'hospital.settings'
    _inherit = 'res.config.settings'

    note = fields.Char(string="", required=False, )
    module_crm = fields.Boolean(string='CRM')
    product_ids = fields.Many2many('product.product', string='Medicines')

    def set_values(self):
        res = super(HospitalSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('odoo_hospital.note', self.note)
        self.env['ir.config_parameter'].set_param('odoo_hospital.module_crm', self.module_crm)
        self.env['ir.config_parameter'].set_param('odoo_hospital.product_ids', self.product_ids.ids)
        return res

    def get_values(self):
        res = super(HospitalSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        notes = ICPSudo.get_param('odoo_hospital.note')
        module_crm = ICPSudo.get_param('odoo_hospital.module_crm')

        product_ids = self.env['ir.config_parameter'].sudo().get_param('odoo_hospital.product_ids')
        res.update(
            note=notes,
            module_crm=module_crm,
            product_ids=[(6, 0, literal_eval(product_ids))],
        )
        return res
