# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MultiCompany(models.Model):
    _name = 'bi.multicompany'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    company_dependent_value_ex = fields.Char(company_dependent=True)
