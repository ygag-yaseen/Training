# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrderConfirm(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        rslt=super(SaleOrderConfirm,self)._action_confirm()

        project = self.env['project.project']
        crm_rec = self.env['crm.lead'].search([('name', '=',self.origin)])
        data = {}
        data = {
            'name'          :crm_rec.name,
            'emp_ids'       :crm_rec.emp_ids
        }
        if not self.env['project.project'].search([('name','=',crm_rec.name)]):
            project.create(data)
            crm_rec.action_set_won()

        return rslt

class CrmProject(models.Model):
    _inherit = 'crm.lead'

    emp_ids = fields.Many2many('hr.employee', string='Employees')
    quotation_count = fields.Integer(compute='_compute_sale_data', string="Number of Quotations")
    
    def action_sale_quotations_new(self):
        rslt=super(CrmProject,self).action_sale_quotations_new()
        return rslt

class ProjectCrm(models.Model):
    _inherit = 'project.project'

    emp_ids = fields.Many2many('hr.employee', string='Employees')