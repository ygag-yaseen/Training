odoo.define('bi_ecommerce.cart', function (require) {
    'use strict';

var publicWidget = require('web.public.widget');
var core = require('web.core');
var _t = core._t;


publicWidget.registry.websiteSaleCartLink = publicWidget.Widget.extend({
    selector: '#top_menu a[href$="/shop/cart"]',


    template: 'product_buy_now1',
    $('.btn1').$click(function(){
        alert("button clicked");
    }),
});

});