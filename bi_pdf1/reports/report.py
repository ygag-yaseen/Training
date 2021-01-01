from odoo import models, fields, api, _
from odoo.tools.misc import xlwt
from odoo.exceptions import UserError, AccessError
import io
import base64
import operator
from PIL import Image
import itertools
import time
from datetime import datetime,timedelta,date
import xlsxwriter


class REPORT5Xlsx(models.AbstractModel):
    _name = 'report.bi_pdf1.report_invoice_docs'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        worksheet = workbook.add_worksheet("INVOICE REPORT")
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True, 'align': 'center', 'bold': True})
        # format12 = workbook.add_format(
        #     {'font_size': 16, 'align': 'center', 'right': True, 'left': True, 'bottom': False,
        #      'top': True, 'bold': True,})
        format3 = workbook.add_format({'bold':True,'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12,'align': 'center'})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12,'bold':True,'align':'center'})
        format3.set_align('center')
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        # boldc = workbook.add_format({'bold':True,'align':'center'})
        center = workbook.add_format({'align':'center'})

        # filter_row = 3
        # filter_row1 = 5
        # if data['form']['start_date']:
        #     start_date = datetime.strptime(data['form']['start_date'], '%Y-%m-%d').date()
        #     worksheet.write('A%s' % filter_row, 'Date From', boldc)
        #     worksheet.write('B%s' % filter_row, str(start_date.strftime("%d-%m-%Y")), boldc)
        # if data['form']['end_date']:
        #     end_date = datetime.strptime(data['form']['end_date'], '%Y-%m-%d').date()
        #     worksheet.write('D%s' % filter_row, 'Date To', boldc)
        #     worksheet.write('E%s' % filter_row, str(end_date.strftime("%d-%m-%Y")), boldc)
            
        row = 4
        new_row = row + 1
        worksheet.set_column('A:A', 7)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 20)
        worksheet.set_column('G:G', 20)
        worksheet.set_column('H:H', 20)
        worksheet.set_column('I:I', 20)
        worksheet.set_column('J:J', 20)


       

        worksheet.merge_range('A1:I1', 'INVOICING REPORT', format3)
        worksheet.write('A%s' % row, 'SL NO', format3)
        worksheet.write('B%s' % row, 'NUMBER', format3)
        worksheet.write('C%s' % row, 'CUSTOMER NAME', format3)
        worksheet.write('D%s' % row, 'INVOICE DATE', format3)
        # worksheet.write('E%s' % row, 'SALES PERSON', format3)
        worksheet.write('E%s' % row, 'DUE DATE', format3)
        worksheet.write('F%s' % row, 'TAX EXCLUDED', format3)
        worksheet.write('G%s' % row, 'TOTAL', format3)
        worksheet.write('H%s' % row, 'AMOUNT DUE', format3)
        worksheet.write('I%s' % row, 'STATUS', format3)
        domain =[]

        # if data['form']['start_date']:
        #     domain.append(('invoice_date', '>=', data['form']['start_date']))
        # if data['form']['end_date']:
        #     domain.append(('invoice_date', '<=', data['form']['end_date']))
           
        start_date = data['form']['start_date']
        end_date = data['form']['end_date']

        # start_date = '11/01/2020'
        # end_date = date.today()

        self.env.cr.execute("""select * from account_move 
                                                 where invoice_date 
                                                 between  '"""+str(start_date)+ """' 
                                                 AND '"""+str(end_date)+"""' """)
        values = self.env.cr.dictfetchall()
                             
        sl_no = 1
        # record = self.env['account.move'].search(domain)
        val = []
    
        for each in values:
           
            worksheet.write('A%s' % new_row, sl_no, center)
            worksheet.write('B%s' % new_row, each['name'])
            worksheet.write('C%s' % new_row, each['invoice_partner_display_name'])
            worksheet.write('D%s' % new_row, each['invoice_date'], center)
            # worksheet.write('E%s' % new_row, each['invoice_user_id'])
            worksheet.write('E%s' % new_row, each['invoice_date_due'], center)
            worksheet.write('F%s' % new_row, each['amount_untaxed_signed'])
            worksheet.write('G%s' % new_row, each['amount_total_signed'])
            worksheet.write('H%s' % new_row, each['amount_residual_signed'])
            worksheet.write('I%s' % new_row, each['state'], center)
            # new_row = new_row + 1
            # worksheet.write('B%s' % new_row, 'quantity',center)
            # worksheet.write('C%s' % new_row, 'product',center)
            # worksheet.write('D%s' % new_row, 'price',center)
            # for k in each.invoice_line_ids:
            #     new_row = new_row + 1
            #     worksheet.write('B%s' % new_row, k.quantity)
            #     # new_row+=1
            #     worksheet.write('C%s' % new_row, k.name)
            #     worksheet.write('D%s' % new_row, k.price_unit)   
            new_row+=1
            sl_no+=1