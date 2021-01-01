# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime,timedelta,date
import base64

class bi_emailtest1(models.Model):
    _name = 'bi.emailtest1'
    # _inherit = 'report.bi_pdf1.report_template'
    _description = 'bi_emailtest1.bi_emailtest1'

    sender = fields.Char(string='From', default='yaseen@bassaminfotech.com')
    recipients_id = fields.Char(string='')
    message_body = fields.Text(string='')
    current_date = fields.Date(string='', default=fields.Date.today)
    attach_file = fields.Binary(string='')

    end_date = date.today()
    start_date = end_date - timedelta(30)

    def action_send_email(self):
        dataa = {
            'form'  : {
                    'start_date': self.start_date,
                    'end_date'  : self.end_date,
                },
            }
        # obj=self.env['invoice.report.wizard']
        pdf = self.env.ref('bi_pdf1.print_report_pdf').render_qweb_pdf(self,data=dataa)
        # obj.print_report_pdf().with_context({'start_date':self.start_date, 'end_date':self.end_date})
        pdfa=base64.b64encode(pdf[0])

        mail_template = self.env.ref('bi_emailtest1.email_template')
        
        # adding attachment------
        attachment = {
                'name': 'file',
                # 'datas': self.attach_file,
                'datas': pdfa,
                'res_model': 'bi.emailtest1',
                'type': 'binary',
                # 'mimetype': 'application/x-pdf'
           }
        
        id1 = self.env['ir.attachment'].create(attachment)
        mail_template.attachment_ids = [(6,0,[id1.id])]

        mail_template.send_mail(self.id, force_send=True)