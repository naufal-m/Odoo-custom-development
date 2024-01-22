from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = "hospital.patient"  # this is model name
    _inherit = ["mail.thread", "mail.activity.mixin"]    # this inheriting mail.thread & mail.activity.mixin model into the om_hospital
    _description = "Patient Records"
    _order = "name desc"

    # describe the fields used in the forms
    # tracking=True is used to tracking the field value changes in the chatter section
    # string values gives the field Label
    """
    field.Selection gives the dropdown. in the selection ('male', 'Male') indicates left one is field technical name,
    and right one is used as value name showing in the dropdown
    """
    name = fields.Char(string='Patient Name', required=True)
    mob = fields.Char(string="Phone Number", tracking=True, required=True)
    address = fields.Char(string="Address", tracking=True)
    reference = fields.Char(
        string="Reference ID",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))
    age = fields.Integer(string="Age")
    is_child = fields.Boolean(string="Is Child", compute="_compute_is_child", store=True)
    notes = fields.Text(string="Notes", tracking=True)
    gender = fields.Selection([
        ('select', 'Select'),
        ('male', 'Male'),
        ('female', 'Female')
    ], required=True, default='select', string="Gender")
    dob = fields.Date(string="DOB")
    blood_group = fields.Selection([
        ('select', 'Select'),
        ('o+', 'O+'),
        ('o-', 'O-'),
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-')
    ], string="Blood Group", default='select', tracking=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancelled', 'Cancelled')
         ], default="draft", string="Status", tracking=True)

    # 'Many2one' type is used for linking a field with another model database. Here 'hr.employee' is another model db.
    # responsible_id = fields.Many2one('hr.employee', string='Reference Doctor')

    appointment_count = fields.Integer(string="Total Appointments", compute='_compute_appointment_count')
    # Add an image field in the patient model
    image = fields.Binary(string='Patient image')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')

    """Compute the appointment count with respect to patient_id"""
    def _compute_appointment_count(self):
        for rec in self:
            patient_appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = patient_appointment_count

    """Compute whether the is_child check box checked based on the age"""
    @api.depends('age')
    def _compute_is_child(self):
        for patient in self:
            patient.is_child = 0 < patient.age <= 15

    def action_confirm(self):
        self.state = 'confirmed'
    def action_done(self):
        self.state = 'done'
    def action_cancelled(self):
        self.state = 'cancelled'
    def action_draft(self):
        self.state = 'draft'

    # Override create method
    @api.model
    def create(self, vals):
        if not vals.get('notes'):   # check if 'notes' field doesn't entered before saving. after saving pass 'New Patient' into 'notes'.
            vals['notes'] = 'New Patient'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalPatient, self).create(vals)
        return res

    """below function is used to check whether name is exist or not. this is also a validation.
    use @api.constrains('variable'). here name need to check"""
    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patient = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patient:
                raise ValidationError(_("Entered patient name %s is already exist." % rec.name))

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if self.age == 0:
                raise ValidationError(_("Age must not be 'zero'.....!"))

    """below function is used to get the name along with reference id. this can get the field use as many2one
    field in other pages"""
    def name_get(self):
        result = []
        for rec in self:
            name = '[' + rec.reference + ']' + " " + rec.name
            result.append((rec.id, name))
        return result
