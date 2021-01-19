odoo.define('bi_pos_button_access.button_access', function (require) {
    "use strict";

var screens = require('point_of_sale.screens');

screens.NumpadWidget.include({

applyAccessRights: function() {
    this._super();
    var cashier = this.pos.get('cashier') || this.pos.get_cashier();
    var has_discount_control_rights = !this.pos.config.restrict_price_control || cashier.role == 'manager';
    this.$el.find('.mode-button[data-mode="discount"]')
        .toggleClass('disabled-mode', !has_discount_control_rights)
        .prop('disabled', !has_discount_control_rights);
    if (!has_discount_control_rights && this.state.get('mode')=='discount'){
        this.state.changeMode('quantity');
    }
},

});

});
