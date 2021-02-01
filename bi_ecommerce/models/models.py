# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class bi_ecommerce(models.Model):
    _name = 'bi.ecommerce'
    _description = 'bi_ecommerce.bi_ecommerce'

    def buy_now1(self):
        raise UserError(_('Button Clicked'))

