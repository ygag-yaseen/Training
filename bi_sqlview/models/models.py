# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class bi_sqlview(models.Model):
    _name = 'bi.sqlview'
    _description = 'bi_sqlview.bi_sqlview'
    _auto = False

    name = fields.Char(string='')
    create_date = fields.Datetime(string='')
    date_order = fields.Datetime(string='')
    partner_id = fields.Many2one('res.partner', string='')
    user_id = fields.Many2one('res.users', string='')
    company_id = fields.Many2one('res.company', string='')
    amount_total = fields.Float(string='')
    state = fields.Char(string='')
    amount_total_invoice = fields.Float(string='')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'bi_sqlview')
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW bi_sqlview AS (
            SELECT 
            row_number() OVER () as id,
                so.name as name, 
                so.create_date as create_date, 
                so.date_order as date_order,
                so.partner_id as partner_id, 
                so.user_id as user_id, 
                so.company_id as company_id,
                so.amount_total as amount_total, 
                so.state as state, 
                am.amount_residual as amount_total_invoice
            FROM sale_order as so 
            JOIN account_move as am ON am.invoice_origin = so.name) ''')