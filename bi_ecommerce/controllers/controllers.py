# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from werkzeug.exceptions import Forbidden, NotFound

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import ValidationError
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.osv import expression

class PartnerForm(http.Controller):
    #mention class name
    @http.route(['/customer/form'], type='http', auth="public", website=True)
    #mention a url for redirection.
    #define the type of controller which in this case is ‘http’.
    #mention the authentication to be either public or user.
    def partner_form(self, **post):
    #create method
    # this will load the form webpage
        return request.render("bi_ecommerce.tmp_customer_form", {})
    @http.route(['/customer/form/submit'], type='http', auth="public", website=True)
    #next controller with url for submitting data from the form#
    def customer_form_submit(self, **post):
        partner = request.env['res.partner'].create({
            'name'  : post.get('name'),
            'email' : post.get('email'),
            'phone' : post.get('phone')
        })
        vals = {
            'partner': partner,
        }
        #inherited the model to pass the values to the model from the form#
        return request.render("bi_ecommerce.tmp_customer_form_success", vals)
        #finally send a request to render the thank you page#