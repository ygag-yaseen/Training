# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import time
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class createpurchaseorder(models.TransientModel):
	_name = 'create.purchaseorder'
	_description = "Create Purchase Order"
	
	new_order_line_ids = fields.One2many('getsale.orderdata', 'new_order_line_id',String="Order Line")
	date_order = fields.Datetime(string='Order Date', required=True, copy=False, default=fields.Datetime.now)

	@api.model
	def default_get(self,  default_fields):
		res = super(createpurchaseorder, self).default_get(default_fields)
		data = self.env['sale.order'].browse(self._context.get('active_ids',[]))
		company = data.company_id
		update = []
		for record in data.order_line:
			quant_id = self.env['stock.quant'].search([('product_id','=',record.product_id.id),('company_id','=',company.id),('quantity','>',record.product_uom_qty)])
			if quant_id.id==False:
				update.append((0,0,{
							'product_id'		: record.product_id.id,
							'product_uom' 		: record.product_uom.id,
							'order_id'			: record.order_id.id,
							'name' 				: record.name,
							'product_qty' 		: record.product_uom_qty,
							'price_unit' 		: record.price_unit,
							'product_subtotal' 	: record.price_subtotal,
							}))
		res.update({'new_order_line_ids':update})
		return res

	def action_create_purchase_order(self):
		data = self.env['sale.order'].browse(self._context.get('active_ids',[]))
		company=data.company_id
		view_context = self.env.context
		allowed_companies = view_context.get('allowed_company_ids', False)
		for i in allowed_companies:
			if i!= company.id:
				self.mycompany2_id=self.env['res.company'].search([('id','=',i)])
		purchase_res = self.env['purchase.order']
		sale_res = self.env['sale.order']
		warehouse_res = self.env['stock.warehouse'].search([('name','=',self.mycompany2_id.name)])
		pvalue = []
		svalue = []
		for data in self.new_order_line_ids:
			sale_order_name = data.order_id.name		
			final_price = data.product_id.standard_price 	
			pvalue.append([0,0,{
				'product_id'	: data.product_id.id,
				'name' 			: data.name,
				'product_qty' 	: data.product_qty,
				'order_id'		: data.order_id.id,
				'product_uom' 	: data.product_uom.id,
				'taxes_id' 		: data.product_id.supplier_taxes_id.ids,
				'date_planned' 	: data.date_planned,
				'price_unit' 	: final_price,
			}])
			svalue.append([0,0,{
				'product_id'		: data.product_id.id,
				'name' 				: data.name,
				'product_uom_qty' 	: data.product_qty,
				'price_unit' 		: final_price,
			}])

		purchase = purchase_res.create({
						'partner_id': self.mycompany2_id.partner_id.id,
						'date_order': str(self.date_order),
						'order_line':pvalue,
						'origin'	: sale_order_name,
						'sale_id'	: self.id
					})

		sale = sale_res.create({
			'partner_id' 	: purchase.company_id.partner_id.id,
			'warehouse_id' 	: warehouse_res.id,
			'company_id' 	: self.mycompany2_id.id,
			'order_line'	: svalue,
					})

		sale_order_id = self.env['sale.order'].browse(self.env.context['active_id'])
		sale_order_id.purchase_order_ids = [(4, purchase.id)]

		return {
            'res_model'	: 'purchase.order',
            'type'		: 'ir.actions.act_window',
            'context'	: {},
            'view_mode'	: 'form',
            'view_type'	: 'form',
			'res_id'	: purchase.id,
            'view_id'	: self.env.ref("purchase.purchase_order_form").id,
            'target'	: 'self'
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
class bi_purchasemulti(models.Model):
	_inherit = 'sale.order'
	 
	purchase_order_ids = fields.Many2many('purchase.order', 'sale_id')
	
	def action_confirm(self):
		company = self.company_id
		records = []
		
		for rec in self.order_line:
			
			quant_id = self.env['stock.quant'].search([('product_id','=',rec.product_id.id),('company_id','=',company.id),('quantity','>',rec.product_uom_qty)])
			records.append(quant_id.id)
		flag = 0
		for i in records:
			if i == False:
				flag = 1
		if flag == 1:

			return {
				'name'		: _('Product not available'),
				'type'		: 'ir.actions.act_window',
				'res_model'	: 'create.purchaseorder',
				'view_mode'	: 'form',
				'target'	: 'new',
			}
		else :
			if self._get_forbidden_state_confirm() & set(self.mapped('state')):
				raise UserError(_(
					'It is not allowed to confirm an order in the following states: %s'
				) % (', '.join(self._get_forbidden_state_confirm())))
			
			for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
				order.message_subscribe([order.partner_id.id])
			self.write({
				'state'		: 'sale',
				'date_order': fields.Datetime.now()
			})

			context = self._context.copy()
			context.pop('default_name', None)

			self.with_context(context)._action_confirm()
			if self.env.user.has_group('sale.group_auto_done_setting'):
				self.action_done()
			return True


#-----------------------------------------------------------------------------------------------
class sales_button(models.Model):
    _inherit = 'purchase.order'

    sale_id = fields.Many2one('sale.order', string='')
# ----------------------------------------------------------------