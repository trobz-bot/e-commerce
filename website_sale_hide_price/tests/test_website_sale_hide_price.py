# Copyright 2024 Tecnativa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase


class TestWebsiteSaleHidePrice(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Disable tracking globally to avoid chatter noise during tests.
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.website = cls.env["website"].create(
            {"name": "Test Website", "domain": "example.com"}
        )
        cls.product = cls.env["product.template"].create(
            {
                "name": "Website Product",
                "list_price": 10.0,
                "website_published": True,
            }
        )

    def test_website_show_price_respects_hide_flag(self):
        self.website.website_hide_price = False
        self.assertTrue(self.website.website_show_price)
        self.website.website_hide_price = True
        self.assertFalse(self.website.website_show_price)

    def test_quick_add_disabled_when_product_price_hidden(self):
        self.website.website_hide_price = False
        self.product.website_hide_price = False
        show_quick_add = self.product.with_context(
            website_id=self.website.id
        )._website_show_quick_add()
        self.assertTrue(show_quick_add)
        self.product.website_hide_price = True
        show_quick_add = self.product.with_context(
            website_id=self.website.id
        )._website_show_quick_add()
        self.assertFalse(show_quick_add)
        self.product.website_hide_price = False
        self.website.website_hide_price = True
        show_quick_add = self.product.with_context(
            website_id=self.website.id
        )._website_show_quick_add()
        self.assertFalse(show_quick_add)
