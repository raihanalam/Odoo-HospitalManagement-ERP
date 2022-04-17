from odoo import api, fields, models

class NewModule(models.Model):
    _name = 'ssnew_module'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char()
    new_field = fields.Binary(string="Test 1")
    is_new_field = fields.Boolean(string="Test 2")
    new_field_id = fields.Many2one(comodel_name="res.user", string="Test 3", required=False, )

    @api.onchange('field_name')
    def onchange_method(self):
        self.field_name = ''

