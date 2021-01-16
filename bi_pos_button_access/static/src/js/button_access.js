odoo.define('bi_pos_button_access.button_access', function (require) {
    "use strict";

var screens = require('point_of_sale.screens');

screens.NumpadWidget.include({

    start: function() {
    this.applyAccessRights();
    this.applyAccessRights1();
    this.state.bind('change:mode', this.changedMode, this);
    this.pos.bind('change:cashier', this.applyAccessRights, this);
    this.pos.bind('change:cashier', this.applyAccessRights1, this);
    this.changedMode();
    this.$el.find('.numpad-backspace').click(_.bind(this.clickDeleteLastChar, this));
    this.$el.find('.numpad-minus').click(_.bind(this.clickSwitchSign, this));
    this.$el.find('.number-char').click(_.bind(this.clickAppendNewChar, this));
    this.$el.find('.mode-button').click(_.bind(this.clickChangeMode, this));
},

    applyAccessRights1: function() {
        var cashier = this.pos.get('cashier') || this.pos.get_cashier();
        var has_price_control_rights = !this.pos.config.restrict_price_control || cashier.role == 'manager';
        this.$el.find('.mode-button[data-mode="discount"]')
            .toggleClass('disabled-mode', !has_price_control_rights)
            .prop('disabled', !has_price_control_rights);
        if (!has_price_control_rights && this.state.get('mode')=='discount'){
            this.state.changeMode('quantity');
        }
    },

    applyAccessRights: function() {
        var cashier = this.pos.get('cashier') || this.pos.get_cashier();
        var has_price_control_rights = !this.pos.config.restrict_price_control || cashier.role == 'manager';
        this.$el.find('.mode-button[data-mode="price"]')
            .toggleClass('disabled-mode', !has_price_control_rights)
            .prop('disabled', !has_price_control_rights);
        if (!has_price_control_rights && this.state.get('mode')=='price'){
            this.state.changeMode('quantity');
        }
    },

    clickDeleteLastChar: function() {
        return this.state.deleteLastChar();
    },
    clickSwitchSign: function() {
        return this.state.switchSign();
    },
    clickAppendNewChar: function(event) {
        var newChar;
        newChar = event.currentTarget.innerText || event.currentTarget.textContent;
        return this.state.appendNewChar(newChar);
    },
    clickChangeMode: function(event) {
        var newMode = event.currentTarget.attributes['data-mode'].nodeValue;
        return this.state.changeMode(newMode);
    },
    changedMode: function() {
        var mode = this.state.get('mode');
        $('.selected-mode').removeClass('selected-mode');
        $(_.str.sprintf('.mode-button[data-mode="%s"]', mode), this.$el).addClass('selected-mode');
    },

});

});
