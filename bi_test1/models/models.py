#-*- coding: utf-8 -*-

from odoo import models, fields, api


class bi_test1(models.Model):
     _name = 'bi.test1'
     _description = 'bi_test1.bi_test1'

     name = fields.Char()
     value = fields.Selection([('one','One'),('two','Two')])
     value2 = fields.Float(compute="_value_pc", store=True)
     description = fields.Text()
     salary1 = fields.Float()
     age1 = fields.Integer()
     path = fields.Char()


     @api.depends('value')
     def _value_pc(self):
         for record in self:
             record.value2 = float(record.value) / 100

     a2 = fields.Many2one('bi.test2')

     state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Cancelled'), ], 
     required=True, default='draft')

     def button_done(self):
          for rec in self:
               rec.write({'state': 'done'})

     def button_reset(self):
          for rec in self:
               rec.state= 'draft'

     def button_cancel(self):
          for rec in self:
               rec.write({'state': 'cancel'})
#create method
     def createb(self):
          for rec in self:
               vals={"salary2":self.salary1,"age2":self.age1}
               self.env['bi.test2'].create(vals)

#write fun
     def writeb(self):
          record_ids = self.env['bi.test1'].search([('name','=','jon')])
          for record in record_ids:
               record.write({
                    'salary1': 1000,
                    'age1': 30,
               })

     def addf(self):
          outFileName="/home/bassam10/path_test/filename.txt"
          outFile=open(outFileName, "w")
          outFile.write("""Hello my name is ABCD""")
          outFile.close()

class bi_test2(models.Model):
     _name = 'bi.test2'
     _description = 'bi_test2.bi_test2'

     a1 = fields.Many2one('bi.test1')
     a3 = fields.One2many('bi.test1','a2')
     a4 = fields.Many2many('bi.test1', string="")
     salary2 = fields.Float(string='')
     age2 = fields.Integer(string='')