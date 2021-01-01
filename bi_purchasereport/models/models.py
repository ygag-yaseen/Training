# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, timedelta, time
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'
 

class ReportWizard(models.TransientModel):
    _name = 'report.wizard'

    product_id1 = fields.Many2one('product.product', string='Product')
    # date_from = fields.Date(string='From')
    # date_to = fields.Date(string='To')

    def printb(self):
        # record_ids = self.env['purchase.order'].search('product_id.name', '==', self.product_id1.name)
        
        record_ids=self.env['purchase.order.line'].search([('product_id', '=', self.product_id1.id)])
        # for each in record_ids:  
        
        if (len(record_ids)==0):
            raise UserError("Product not found")


        return self.env.ref('bi_purchasereport.print_report_pdf').report_action(record_ids)

        


        # Date comparing------------
        # record_ids = self.env['purchase.order'].search([('date_order', '>=', self.date_from),('date_order', '<=', self.date_to)])
