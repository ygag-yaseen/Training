# -*- coding: utf-8 -*-
from odoo import models, fields, api
import time
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class createpurchaseorder(models.TransientModel):
	_name = 'create.purchaseorder'
	_description = "Create Purchase Order"

	new_order_line_ids = fields.One2many( 'getsale.orderdata', 'new_order_line_id',String="Order Line")
	partner_id = fields.Many2one('res.partner', string='Vendor', required = True)
	date_order = fields.Datetime(string='Order Date', required=True, copy=False, default=fields.Datetime.now)
	mycompany_id = fields.Many2one('res.company', string='Company')

	@api.model
	def default_get(self,  default_fields):
		res = super(createpurchaseorder, self).default_get(default_fields)
		data = self.env['sale.order'].browse(self._context.get('active_ids',[]))
		update = []
		for record in data.order_line:
			update.append((0,0,{
							'product_id' : record.product_id.id,
							'product_uom' : record.product_uom.id,
							'order_id': record.order_id.id,
							'name' : record.name,
							'product_qty' : record.product_uom_qty,
							'price_unit' : record.price_unit,
							'product_subtotal' : record.price_subtotal,
							}))
		res.update({'new_order_line_ids':update})
		return res

	def action_create_purchase_order(self):
		res = self.env['purchase.order']
		value = []
		for data in self.new_order_line_ids:
			sale_order_name = data.order_id.name		
			final_price = data.product_id.standard_price 	
			value.append([0,0,{
								'product_id' : data.product_id.id,
								'name' : data.name,
								'product_qty' : data.product_qty,
								'order_id':data.order_id.id,
								'product_uom' : data.product_uom.id,
								'taxes_id' : data.product_id.supplier_taxes_id.ids,
								'date_planned' : data.date_planned,
								'price_unit' : final_price,
								'company_id' : self.mycompany_id.id
								}])
		purchase = res.create({
						'partner_id' : self.partner_id.id,
						'date_order' : str(self.date_order),
						'order_line':value,
						'origin' : sale_order_name,
					})

		sale_order_id = self.env['sale.order'].browse(self.env.context['active_id'])
		sale_order_id.purchase_order_ids = [(4, purchase.id)]

		return {
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'context': {},
            'view_mode': 'form',
            'view_type': 'form',
			'res_id': purchase.id,
            'view_id': self.env.ref("purchase.purchase_order_form").id,
            'target': 'self'
        }
#-----------------------------------------------------------------------------------------------
class Getsaleorderdata(models.TransientModel):
	_name = 'getsale.orderdata'
	_description = "Get Sale Order Data"

	new_order_line_id = fields.Many2one('create.purchaseorder')
		
	product_id = fields.Many2one('product.product', string="Product", required=True)
	name = fields.Char(string="Description")
	product_qty = fields.Float(string='Quantity', required=True)
	date_planned = fields.Datetime(string='Scheduled Date', default = datetime.today())
	product_uom = fields.Many2one('uom.uom', string='Product Unit of Measure')
	order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
	price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
	product_subtotal = fields.Float(string="Sub Total", compute='_compute_total')
	
	@api.depends('product_qty', 'price_unit')
	def _compute_total(self):
		for record in self:
			record.product_subtotal = record.product_qty * record.price_unit
#-----------------------------------------------------------------------------------------------
class bi_purchasebutton(models.Model):
	_inherit = 'sale.order'
	 
	purchase_order_ids = fields.Many2many('purchase.order', 'sale_id')
	purchase_order_count = fields.Char(compute='compute_count_purchase') 

	@api.depends('purchase_order_ids')
	def compute_count_purchase(self):
		self.purchase_order_ids = self.mapped('purchase_order_ids')
		for record in self:
			record.purchase_order_count = len(record.purchase_order_ids)

	def purchase_order(self):
		purchase_order_ids = self.mapped('purchase_order_ids')

		if len( purchase_order_ids) > 1:
			return {
                'name': ('Purchase Order'),
                'type': 'ir.actions.act_window',
                'res_model':'purchase.order',
                'view_mode':'tree,form',
                'domain': [('id', 'in', self.purchase_order_ids.ids)],
                'target':'current',
            }
			
		elif len(purchase_order_ids) == 1:
			return {
                'name': ('Purchase Order'),
                'type': 'ir.actions.act_window',
                'res_model':'purchase.order',
                'view_mode':'form',
                'res_id': self.purchase_order_ids.id,
                'target':'current',
         }

		elif len(purchase_order_ids) == 0:
			raise UserError("No Purchase Order Found")
#-----------------------------------------------------------------------------------------------
class sales_button(models.Model):
    _inherit = 'purchase.order'

    sale_id = fields.Many2one('sale.order', string='')