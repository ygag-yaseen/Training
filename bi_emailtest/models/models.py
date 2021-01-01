# -*- coding: utf-8 -*-
import odoo
from odoo import models, fields, api, _
from datetime import date



class bi_emailtest(models.Model):

    _inherit = 'sale.order'
    _description = 'bi_emailtest.bi_emailtest'

    sender_id = fields.Many2one('res.users', string='', default= lambda self: self.env.user)
    

    

    def action_send_email(self):
#-------------------------------------------------------------------------------
# MAIL DIRECT 
        mail_template = self.env.ref('bi_emailtest.email_template11')
        mail_template.send_mail(self.id, force_send=True)
# ------------------------------------------------------------------------------
# MAIL WIZARD
    #     self.ensure_one()
    #     ir_model_data = self.env['ir.model.data']
    #     try:
    #         template_id = \
    #         ir_model_data.get_object_reference('bi_emailtest', 'email_template')[1]
    #     except ValueError:
    #         template_id = False
    #     try:
    #         compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
    #     except ValueError:
    #         compose_form_id = False
    #     ctx = {
    #     'default_model': 'sale.order',
    #     'default_res_id': self.ids[0],
    #     'default_use_template': bool(template_id),
    #     'default_template_id': template_id,
    #     'default_composition_mode': 'comment',
    # }
    #     return {
    #     'name': _('Compose Email'),
    #     'type': 'ir.actions.act_window',
    #     'view_mode': 'form',
    #     'res_model': 'mail.compose.message',
    #     'views': [(compose_form_id, 'form')],
    #     'view_id': compose_form_id,
    #     'target': 'new',
    #     'context': ctx,
    # }
# --------------------------------------------------------------------------------------