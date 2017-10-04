from datetime import date, datetime, timedelta

import pytest

from ordreset import d
from ordreset.db import declarative as decl, interface


class TestGetOrders:
    def test_ok(self):
        psc1 = decl.ProcStateCodes(1, 'psc1')
        psc2 = decl.ProcStateCodes(2, 'psc2')

        ec1 = decl.ErrorCodes(11, 'ec1')
        ec2 = decl.ErrorCodes(12, 'ec2')

        d.session.add(decl.InterfaceEvent(1, psc1, ec1))
        d.session.add(decl.InterfaceEvent(2, psc2, ec2))
        d.session.add(decl.InterfaceEvent(3, psc1))
        d.session.add(decl.InterfaceEvent(4))

        assert interface.get_orders() == [
                {
                    'id': 1,
                    'eventTime': None,
                    'partner': None,
                    'msgType': None,
                    'procEnv': None,
                    'procStateDesc': 'psc1',
                    'procMsg': None,
                    'procResDesc': 'ec1',
                },
                {
                    'id': 2,
                    'eventTime': None,
                    'partner': None,
                    'msgType': None,
                    'procEnv': None,
                    'procStateDesc': 'psc2',
                    'procMsg': None,
                    'procResDesc': 'ec2',
                },
                {
                    'id': 3,
                    'eventTime': None,
                    'partner': None,
                    'msgType': None,
                    'procEnv': None,
                    'procStateDesc': 'psc1',
                    'procMsg': None,
                    'procResDesc': None,
                },
            ]
