from odoo import models, fields, api

class SaleReportWizard(models.TransientModel):
        _name = 'sale.report.wizard'
        
        start_date = fields.Date(string='Start Date',required=True)
        end_date = fields.Date(string='End Date',required=True)
        
        def print_report_xl(self):
            # data = {'start_date': self.start_date, 'end_date': self.end_date}
            context = self._context
            datas = {'ids': context.get('active_ids', [])}
            datas['form'] = self.read()[0]
            for field in datas['form'].keys():
                if isinstance(datas['form'][field], tuple):
                    datas['form'][field] = datas['form'][field][0]
            return self.env.ref('bi_xlreport.report_sale_docs').report_action(self, data=datas)