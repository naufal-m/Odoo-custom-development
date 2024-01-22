from odoo import api, fields, models


class schoolTeacher(models.Model):
    _name = "school.teacher"
    _inherit = 'mail.thread'
    _description = 'Teacher Records'
    _rec_name = 'ref'

    name = fields.Char(string='Name', required=True, tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')],
                              string='Gender', tracking=True)
    ref = fields.Char(string='Reference', required=True)

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, f'{rec.ref} - {rec.name}'))
        return res
