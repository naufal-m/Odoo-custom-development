from odoo import api, fields, models, _


class CreateAppointmentWiz(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    date_appointment = fields.Datetime(string="Date of appointment", required=True)

    """
        below function is used to create an appointment by clicking created button from wizard """

    def action_create_appointment(self):
        print("Button clicked")
        vals = {
            "patient_id": self.patient_id.id,
            "date_appointment": self.date_appointment,
        }
        print("vals..................", vals)
        appointment_rec = self.env['hospital.appointment'].create(vals)
        print("appointment", appointment_rec)

        """ Below code used to returning appointment view form with data after create appointment from the wizard
        'target' set as 'new' means, returning to a wizard style appointment form. if not using the target, then
        returning to default appointment form view"""
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
            # 'target': 'new',
        }
