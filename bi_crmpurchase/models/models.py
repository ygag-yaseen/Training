from odoo import models, fields, api
import time
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class bi_purchasebutton1(models.Model):
    _inherit = 'crm.lead'


class project_test(models.TransientModel):
    _name = 'project.test'
    _description = ""
    
    product_id = fields.Many2one('product.product',string='Product')
    partner_id = fields.Many2one('res.partner',string='Vendor Name')
    qty = fields.Integer(string='Quantity')
    name = fields.Char(string='Description')
    price_unit = fields.Integer(string='Unit Price')
    # company_id=fields.Many2one('res.company',string='company name')
    def button1(self):
        record = self.env['purchase.order']
        new_lines =[]
        new_lines.append((0, 0, {
            'product_id':self.product_id.id,
            'product_qty':self.qty,
            'name':self.name,
            'price_unit':self.price_unit
        }))
        data= {
            'partner_id':self.partner_id.id,
            'order_line':new_lines,
			
            # 'company_id':self.company_id.id
        }
        sale = record.create(data)
        return True