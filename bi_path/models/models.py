# -*- coding: utf-8 -*-

from odoo import models, fields, api, os


class bi_path(models.Model):
    _name = 'bi.path'
    _description = 'bi_path.bi_path'

    name = fields.Char()
    value = fields.Integer()
    path = fields.Char()

    def addf(self):
        for rec in self:
            outFileName=(rec.path)
            outFile=open(outFileName, "w")
            outFile.write(rec.name)
            outFile.write("\n")
            outFile.write(str(rec.value))
            outFile.close()

    def addr(self):
        for rec in self:
            with open(rec.path) as file:   
                data = file.readlines()
                # line = file.readline()
                for line in data:
                    data1 = line.split()
                    self.env['bi.path'].create({'name': data1[0], 'value': data1[1]})
                file.close()