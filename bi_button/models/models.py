#-*- coding: utf-8 -*-
from odoo import models, fields, api
class ToDo(models.Model):    
    _name = 'to.do'    
    _rec_name = 'title'    
    _description = 'Todo'    
    title = fields.Char(string='Title', required=True)    
    description = fields.Html(string='Description')    
    progress_state = fields.Selection(
        [('To do'),('In progress'),('Done')],        
    string='State',        
    default='todo'    )

    def set_done(self):        
        self.write({            
            # We update the state of the statusbar (selection) field by setting the key value.            
            'progress_state': 'done'        })