from odoo import api, fields, models, _

class HospitalDepartment(models.Model):
    _name = "hospital.department"  # this is model name
    _inherit = ["mail.thread", "mail.activity.mixin"]    # this inheriting mail.thread & mail.activity.mixin model into the om_hospital
    _description = "Department Records"

    name = fields.Char(string='Department Name', required=True)
    reference = fields.Char(
        string="Order Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))
    notes = fields.Text(string="Notes", tracking=True)
    # Add an image field in the patient model
    image = fields.Binary(string='Doctor image', copy=False)

    # Override create method
    @api.model
    def create(self, vals):
        if not vals.get(
                'notes'):  # check if 'notes' field doesn't entered before saving. after saving pass 'New Department' into 'notes'.
            vals['notes'] = 'New Department'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.department') or _('New')
        res = super(HospitalDepartment, self).create(vals)
        return res

    # below def copy method is used to duplicating the record with additional term of (COPY) on name field
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _('%s (COPY)', self.name)
            default['notes'] = "Record copied"
        return super(HospitalDepartment, self).copy(default)
