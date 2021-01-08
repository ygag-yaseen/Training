# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime



class bi_stock_tracking(models.Model):
    _name ='bi.stock.tracking'
    _description = "Picking Type"
    _rec_name = 'sequence_no'
    
# -----Location----
    picking_from_id=fields.Many2one('stock.location',string='Source')
    transit_id=fields.Many2one('stock.location',string='Transit')
    dest_location_id=fields.Many2one('stock.location',string='Destination')     
    company_id = fields.Many2one('res.company', 'Company', required=True,default=lambda s: s.env.company.id, index=True)
# -----Other---
    name = fields.Char(string='Reference')
    operation_type_id=fields.Many2one('stock.picking.type',string='Operation Type')
    scheduled_date=fields.Datetime(string="Date",default=datetime.datetime.now())
    move_type = fields.Selection([('direct', 'As soon as possible'), ('one', 'When all products are ready')], 'Shipping Policy')
    description_picking = fields.Text('Description of Picking',default="Internal Transfer")
    move_line_ids = fields.Many2many('stock.move.line') 
    state = fields.Selection([
            ('draft', 'Draft'),
            ('reserved', 'Reserved'),
            ('transfered', 'Transfered'),
            ],default='draft')
# -----sequence_no--------
    sequence_no = fields.Char('sequence_no', readonly=True,default='New')

    @api.model
    def create(self, vals):
        if vals.get('sequence_no', 'New') == 'New':
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code('bi.stock.tracking') or '/'
        return super(bi_stock_tracking, self).create(vals)
# -----Products
    product_id=fields.Many2one('product.product',string='Product')
    qty_reserve=fields.Integer(string='To Reserve')
    qty_demand=fields.Integer(string='Initial Demand')
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', required=True, )
    
    def reserve(self):
        record = self.env['stock.picking']
        new_lines =[]
        new_lines.append((0, 0, {
            'product_id'            :self.product_id.id,
            'product_uom_qty'       :self.qty_reserve,
            'description_picking'   :self.description_picking,
            'name'                  :self.product_id.name,            
            'product_uom'           :1,
              }))

        pick = {}
        pick = {
            'picking_type_id'           :self.operation_type_id.id,
            'name'                      :record.product_id.display_name,
            'location_dest_id'          :self.transit_id.id,
            'location_id'               :self.picking_from_id.id,
            'move_ids_without_package'  :new_lines,
            'move_type'                 :self.move_type,
            'company_id'                :self.company_id.id,
            'scheduled_date'            :self.scheduled_date  
        }

        picking =record.create(pick)            
        picking.action_confirm()
        picking.action_assign()
        picking.button_validate() 

        move = self.env['stock.move'].create({
            'name'              :self.sequence_no,
            'location_id'       :self.picking_from_id.id,
            'location_dest_id'  :self.transit_id.id,
            'product_id'        :self.product_id.id,
            'product_uom'       :self.product_uom_id.id,
            'product_uom_qty'   :self.qty_reserve,
        })

        move._action_confirm()
        move._action_assign()
        move.move_line_ids.write({'qty_done':self.qty_reserve}) 
        move._action_done()

        self.write({
        'state': 'reserved',})

    def validate(self):
        record = self.env['stock.picking']
        new_lines =[]
        new_lines.append((0, 0, {
            'product_id'            :self.product_id.id,
            'product_uom_qty'       :self.qty_demand,
            'description_picking'   :self.description_picking,
            'name'                  :self.product_id.name,
            'product_uom'           : 1,
              }))

        pick = {}  
        pick = {
            'picking_type_id'           :self.operation_type_id.id,
            'name'                      :record.product_id.display_name,
            'location_dest_id'          :self.dest_location_id.id,
            'location_id'               :self.transit_id.id,
            'move_ids_without_package'  :new_lines,
            'move_type'                 :self.move_type,
            'company_id'                :self.company_id.id,
            'scheduled_date'            :self.scheduled_date
        }

        picking =record.create(pick)

        move = self.env['stock.move'].create({
            'name'              :self.sequence_no,
            'location_id'       :self.transit_id.id,
            'location_dest_id'  :self.dest_location_id.id,
            'product_id'        :self.product_id.id,
            'product_uom'       :self.product_uom_id.id,
            'product_uom_qty'   :self.qty_demand,
        })

        move._action_confirm()
        move._action_assign()
        move.move_line_ids.write({'qty_done':self.qty_demand}) 
        move._action_done()

        picking.action_confirm()
        picking.action_assign()
        picking.button_validate()

        self.write({
        'state': 'transfered',})