from odoo import models, fields, api

class HospitalSettings(models.TransientModel):
    #_name = 'hospital.settings'
    _inherit = 'res.config.settings'

    note = fields.Char(string="", required=False, )
    module_crm = fields.Boolean(string='CRM')

    def set_values(self):
        res = super(HospitalSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('odoo_hospital', self.note)
        return res

    def get_values(self):
        res = super(HospitalSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        notes = ICPSudo.get_param('odoo_hospital.note')
        res.update(
            note=notes
        )
        return res
