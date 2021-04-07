'use strict';
odoo.define('website_sale_payment_discount.checkout', function (require) {

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var model = require('website_sale_delivery.checkout');
    var _t = core._t;

    console.log(model);

    var $pay_button = $('#o_payment_form_pay');

    var _onPayClick = function(ev) {
        $pay_button.data('disabled_reasons', $pay_button.data('disabled_reasons') || {});
        $pay_button.data('disabled_reasons').carrier_selection = true;
        $pay_button.prop('disabled', true);
        var payment_id = $(ev.currentTarget).val().replace('form_', '')
        console.log(payment_id);
        var values = {'payment_id': payment_id};
        ajax.jsonRpc('/shop/update_payment', 'call', values).then(_onPaymentUpdateAnswer);
    };

    var _onPaymentUpdateAnswer = function(result) {
	console.log('Payment Change');
	console.log(result);
        var $amount_delivery = $('#order_delivery span.oe_currency_value');
        var $amount_untaxed = $('#order_total_untaxed span.oe_currency_value');
        var $amount_tax = $('#order_total_taxes span.oe_currency_value');
        var $amount_total = $('#order_total span.oe_currency_value');
        var $discount = $('#order_discounted');
        var $amount_delivery = $('#order_payment span.oe_currency_value');

        if (result.status === true) {
            $amount_delivery.text(result.new_amount_delivery);
            $amount_untaxed.text(result.new_amount_untaxed);
            $amount_tax.text(result.new_amount_tax);
            $amount_total.text(result.new_amount_total);
            $amount_delivery.text(result.discount);
            $pay_button.data('disabled_reasons').carrier_selection = false;
            $pay_button.prop('disabled', _.contains($pay_button.data('disabled_reasons'), true));
        }
        else {
            $amount_delivery.text(result.new_amount_delivery);
            $amount_untaxed.text(result.new_amount_untaxed);
            $amount_tax.text(result.new_amount_tax);
            $amount_total.text(result.new_amount_total);
            $amount_delivery.text(result.discount);
        }
    };

    var $pays = $("#payment_method input[name='pm_id']");
    $pays.click(_onPayClick);

    if ($pays.length > 0) {
        $pays.filter(':checked').click();
    }

});
