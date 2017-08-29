from datetime import date, datetime, timedelta

import pytest

from ordreset import d
from ordreset.db import declarative as decl, interface


class TestGetPiecesPerOrder:
    def test_group_by(self):
        pa1 = decl.Partner('pa1')

        oh1 = decl.OrderHeader('en1', pa1, 'or1')
        oh2 = decl.OrderHeader('en1', pa1, 'or2')

        os1 = decl.OrderStore(oh1, 'sl1')
        os2 = decl.OrderStore(oh1, 'sl2')
        os3 = decl.OrderStore(oh2, 'sl1')

        d.session.add(decl.OrderLine(os1, 1, 1))
        d.session.add(decl.OrderLine(os1, 2, 2))
        d.session.add(decl.OrderLine(os2, 1, 4))
        d.session.add(decl.OrderLine(os2, 2, 8))
        d.session.add(decl.OrderLine(os3, 1, 16))
        d.session.add(decl.OrderLine(os3, 2, 32))

        assert interface._get_pieces_per_order('pa1', []) == {
            'orders': 3, 'units': 63}

    def test_order_store_without_line(self):
        pa1 = decl.Partner('pa1')

        oh1 = decl.OrderHeader('en1', pa1, 'or1')
        oh2 = decl.OrderHeader('en1', pa1, 'or2')

        os1 = decl.OrderStore(oh1, 'sl1')
        os2 = decl.OrderStore(oh2, 'sl2')
        d.session.add(os2)

        d.session.add(decl.OrderLine(os1, 1, 1))

        assert (
            interface._get_pieces_per_order('pa1', [])['orders'] == 1)
