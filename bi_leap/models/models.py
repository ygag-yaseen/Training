# -*- coding: utf-8 -*-

import logging
import math

from collections import namedtuple

from datetime import datetime, date, timedelta, time
from pytz import timezone, UTC

from odoo import api, fields, models, SUPERUSER_ID, tools
from odoo.addons.base.models.res_partner import _tz_get
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_compare
from odoo.tools.float_utils import float_round
from odoo.tools.translate import _
from odoo.osv import expression

class hr_wizard(models.TransientModel):

    _name = 'hr.wizard'

    _description = 'HR employee wizard'

    message = fields.Text(string="Timeoff cannot be approved", readonly=True, store=True)

class bi_leap(models.Model):
    _inherit = 'hr.leave'

    # asd = fields.Char(string='')


    def action_approve(self):
        rslt=super(bi_leap,self).action_approve()

        record = self.env['hr.leave'].search(['|',('request_date_from','=',self.request_date_from),('request_date_to','=',self.request_date_to)])
        if (len(record)==3):
            raise UserError(_("Error1"))
    #         return {

    # 'name': 'Error',

    # 'type': 'ir.actions.act_window',

    # 'res_model': 'hr.wizard',

    # 'view_mode': 'form',

    # 'view_type': 'form',

    # 'target': 'current'

    #   }
            # self.write({ 'state' : 'refuse'})
            # return {'value':{},'warning':{'title':'warning','message':'Your message'}}

            

        # list1 =[]
        # for each in record:
        #     for n in range((each.request_date_to - each.request_date_from).days):
        #         date = each.request_date_from + timedelta(n)
        #         list1.append(date)
        #         for holiday in self:
        #             for n in range((holiday.request_date_to - holiday.request_date_from).days):
        #                 date = holiday.request_date_from + timedelta(n)
        #                 self.date_list.append(date)
                        
        return rslt