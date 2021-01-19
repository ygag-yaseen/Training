# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
# from odoo.exceptions import UserError

class bi_dupe(models.Model):
    _name = 'bi.dupe'
    _description = 'bi_dupe.bi_dupe'


    source_document = fields.Reference(selection='_select_target_model', string="Source Document")
    count = fields.Integer(string='')
    intervel = fields.Selection([('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],  default='daily')
    now = fields.Datetime(string='',default=datetime.now())
    i = fields.Integer(string='', default=0)

    @api.model
    def _select_target_model(self):   
        models = self.env['ir.model'].search([])
        return [(model.model, model.name) for model in models]

    def goo(self):
        rec = self.env['bi.dupe'].search([],order='id desc')[0]
        record = rec.source_document._name
        cron = self.env['ir.cron']
        if rec.i < rec.count:
            if rec.intervel == 'daily':
                self.env[record].browse(rec.source_document.id).copy(default={'id':rec.source_document.id})
                rec.i+=1
                rec.now += timedelta(days=1)
                cron.nextcall = rec.now

            if rec.intervel == 'weekly':
                self.env[record].browse(rec.source_document.id).copy(default={'id':rec.source_document.id})
                rec.i+=1
                rec.now += timedelta(days=7)
                cron.nextcall = rec.now

            if rec.intervel == 'monthly':
                self.env[record].browse(rec.source_document.id).copy(default={'id':rec.source_document.id})
                rec.i+=1
                rec.now += timedelta(days=30)
                cron.nextcall = rec.now

