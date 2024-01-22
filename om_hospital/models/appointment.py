from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"  # this is model name
    _inherit = ["mail.thread",
                "mail.activity.mixin"]  # this inheriting mail.thread & mail.activity.mixin model into the om_hospital
    _description = "Hospital Appointment"
    _order = "name desc"

    # describe the fields used in the forms
    # tracking=True is used to tracking the field value changes in the chatter section
    # string values gives the field Label
    """
    field.Selection gives the dropdown. in the selection ('male', 'Male') indicates left one is field technical name,
    and right one is used as value name showing in the dropdown
    """
    name = fields.Char(
        string="Order Reference",
        required=True, copy=False, readonly=True,
        default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    # below doctor_id field is called from doctor model by using Many2one method with model name 'hospital.doctor'
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    state = fields.Selection([
            ('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancelled', 'Cancelled')
         ], default="draft", string="Status", tracking=True)
    notes = fields.Text(string="Notes", related='patient_id.notes', tracking=True)
    date_appointment = fields.Datetime(string="Date of appointment")
    date_checkup = fields.Datetime(string="Checkup Time")
    """
    below codes are related field. automatically displaying the 'age' and 'mob' based on selecting 'patient_id'.
    Here 'patient_id' is Many2one field from 'hospital.patient' model.
    """
    age = fields.Integer(string="Age", related='patient_id.age', tracking=True)
    mob = fields.Char(string="Phone Number", related='patient_id.mob', tracking=True, required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender', related='patient_id.gender', tracking=True)
    prescription_ids = fields.One2many("appointment.prescription.lines", "appointment_id", string='Prescription')
    # One2many is specifying by ("model", "relational field", string="field_name")
    tests_line_ids = fields.One2many('appointment.tests.lines', 'appointment_id', string='Tests taken')
    doctor_remarks = fields.Text(string='Remarks')

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancelled(self):
        self.state = 'cancelled'

    @api.model
    def create(self, vals):
        if not vals.get(
                'notes'):  # check if 'notes' field doesn't entered before saving. after saving pass 'New Patient' into 'notes'
            vals['notes'] = 'New Appointment'
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        return res

    # below function is used to validate the delete action based on the condition. for validation, use ValidateError
    def unlink(self):
        print("delete action called")
        if self.state == 'done' or self.state == 'confirmed':
            raise ValidationError(_("Unable to delete %s. Only Draft or Cancelled state can delete." %self.name))
        return super(HospitalAppointment, self).unlink()

    """ choose gender and notes, based on the patient id changes. I comment this function,
    because gender and notes are not called while appointment created from wizard. otherwise its called """
    # @api.onchange('patient_id')
    # def onchange_patient_id(self):
    #     if self.patient_id:
    #         if self.patient_id.gender:
    #             self.gender = self.patient_id.gender
    #         if self.patient_id.notes:
    #             self.notes = self.patient_id.notes
    #     else:
    #         self.gender = ''
    #         self.notes = ''



class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"  # this is model name
    _description = "Appointment prescription lines"

    name = fields.Char(string='Medicine')
    qty = fields.Integer(string='No.of times')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')

class AppointmentTestsLines(models.Model):
    _name = "appointment.tests.lines"  # this is model name
    _description = "Appointment tests lines"

    name = fields.Char(string='Test name')
    qty = fields.Integer(string='No.of times')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
