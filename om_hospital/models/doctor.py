from odoo import api, fields, models, _

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"  # this is model name
    _inherit = ["mail.thread", "mail.activity.mixin"]    # this inheriting mail.thread & mail.activity.mixin model into the om_hospital
    _description = "Doctor Records"

    name = fields.Char(string='Doctor Name', required=True)
    mob = fields.Char(string="Phone Number", tracking=True, copy=False)
    address = fields.Char(string="Address", tracking=True, copy=False)
    reference = fields.Char(
        string="Order Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))
    age = fields.Integer(string="Age", copy=False)
    notes = fields.Text(string="Notes", tracking=True)
    gender = fields.Selection([
        ('select', 'Select'),
        ('male', 'Male'),
        ('female', 'Female')
    ], required=True, default='select', string="Gender")
    dob = fields.Date(string="DOB", copy=False)
    # Add an image field in the patient model
    image = fields.Binary(string='Doctor image', copy=False)
    department_id = fields.Many2one('hospital.department', string='Department')

    # Override create method
    @api.model
    def create(self, vals):
        if not vals.get(
                'notes'):  # check if 'notes' field doesn't entered before saving. after saving pass 'New Doctor' into 'notes'.
            vals['notes'] = 'New Doctor'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.doctor') or _('New')
        res = super(HospitalDoctor, self).create(vals)
        return res

    # below def copy method is used to duplicating the record with additional term of (COPY) on name field
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _('%s (COPY)', self.name)
            default['notes'] = "Record copied"
        return super(HospitalDoctor, self).copy(default)
