from odoo import api, fields, models, _


class ViewAppointmentWiz(models.TransientModel):
    _name = "view.appointment.wizard"
    _description = "View Appointment Wizard"

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)

    """below function returns the search appointment based on the patient_id by using either 1st or 2nd action and use
    different return methods. either directly call action in return or give all necessary info to the return as dict."""

    def action_view_appointment(self):
        # action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
        action = self.env['ir.actions.actions']._for_xml_id("om_hospital.action_hospital_appointment")
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Appointments',
        #     'res_model': 'hospital.appointment',
        #     'view_type': 'form',
        #     'view_mode': 'tree, form',
        #     'domain': [('patient_id', '=', self.patient_id.id)],
        #     'target': 'current',
        # }
