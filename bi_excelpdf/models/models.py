from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError
import datetime

class SaleReportWizard(models.TransientModel):
        _name = 'invoice.report.wizard'
        
        start_date = fields.Date(string='Start Date',required=True)
        end_date = fields.Date(string='End Date',default=fields.Date.today)
        
        def print_report_xl(self):
            
            record_ids = self.env['account.move'].search([('invoice_date', '>=', self.start_date),('invoice_date', '<=', self.end_date)])
            if len(record_ids)== 0:
                raise UserError("No Data Found") 
            else:
                context = self._context
                datas = {'ids': context.get('active_ids', [])}
                datas['form'] = self.read()[0]
                # for field in datas['form'].keys():
                #     if isinstance(datas['form'][field], tuple):
                #         datas['form'][field] = datas['form'][field][0]
                return self.env.ref('bi_excelpdf.report_invoice_docs').report_action(self, data=datas)

        def print_report_pdf(self):
            # start_date = datetime.datetime.strptime(str(self.start_date), '%Y-%m-%d').strftime('%Y-%m-%d')
            # end_date = datetime.datetime.strptime(str(self.end_date), '%Y-%m-%d').strftime('%Y-%m-%d')

            data = {
            'ids'   : self.ids,
            'model' : self._name,
            'form'  : {
                    'start_date': self.start_date,
                    'end_date'  : self.end_date,
                },
            }

            record_ids = self.env['account.move'].search([('invoice_date', '>=', self.start_date),('invoice_date', '<=', self.end_date)])
          
            if len(record_ids)== 0:
                raise UserError("No Data Found")
            else:
                return self.env.ref('bi_excelpdf.print_report_pdf').report_action(self,data=data)

class BiPDFReport(models.AbstractModel):

    _name = 'report.bi_excelpdf.report_template'

    @api.model
    def _get_report_values(self, docids, data):

        start_date = data['form']['start_date']
        end_date = data['form']['end_date']

        self.env.cr.execute(""" select am.name as id, am.invoice_partner_display_name, rp.name as name, am.invoice_date, am.invoice_date_due, am.amount_untaxed_signed, am.amount_total_signed, am.amount_residual_signed, am.state
                                from account_move am
                                INNER JOIN res_users ru ON am.invoice_user_id = ru.id
                                join res_partner rp on rp.id = ru.partner_id
                                where invoice_date 
                                between  '"""+str(start_date)+ """' 
                                AND '"""+str(end_date)+"""' """)
        values = self.env.cr.dictfetchall()
        return {
                'values' : values,
                }