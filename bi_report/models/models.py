

from odoo import models, fields, api


class bi_report(models.Model):
    _name = 'bi.report'
    _description = 'bi_report.bi_report'

    name = fields.Char()
    name1 = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    
    
    @api.onchange('name')
    def _onchange_(self):
        self.name1 = "Mr." + self.name
        

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100


