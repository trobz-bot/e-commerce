# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.osv.expression import Domain
from odoo.http import request


class Website(models.Model):
    _inherit = "website"

    website_hide_price = fields.Boolean(
        string="Hide prices on website",
        copy=False,
        help="Hide price at website level",
    )
    website_show_price = fields.Boolean(
        compute="_compute_website_show_price",
        search="_search_website_show_price",
    )
    website_hide_price_default_message = fields.Char(
        string="Default Hidden price message",
        help="When the price is hidden on the website we can give the customer"
        "some tips on how to find it out.",
        translate=True,
    )

    def _get_current_partner_show_price(self):
        try:
            return request.env.user.partner_id.website_show_price
        except (AttributeError, RuntimeError):
            return self.env.user.partner_id.website_show_price

    def _compute_website_show_price(self):
        partner_show_price = self._get_current_partner_show_price()
        for rec in self:
            rec.website_show_price = not rec.website_hide_price and partner_show_price

    def _search_website_show_price(self, operator, value):
        if operator not in ("in", "not in") or True not in value:
            return NotImplemented
        partner_show_price = self._get_current_partner_show_price()
        if not partner_show_price:
            return Domain([("id", "=", False)]) if operator == "in" else Domain([])
        hide_price = operator == "not in"
        return Domain([("website_hide_price", "=", hide_price)])
