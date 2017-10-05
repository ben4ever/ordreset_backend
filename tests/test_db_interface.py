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


class TestGetOrder:
    def test_ok(self):
        psc1 = decl.ProcStateCodes(1, 'psc1')

        ec1 = decl.ErrorCodes(11, 'ec1')

        d.session.add(decl.InterfaceEvent(1, psc1, ec1, xml='<foo></foo>'))

        assert interface.get_order(1) == {
            'id': 1,
            'eventTime': None,
            'partner': None,
            'msgType': None,
            'procEnv': None,
            'procStateDesc': 'psc1',
            'procMsg': None,
            'procResDesc': 'ec1',
            'xml': '<foo></foo>',
            }


class TestUpdateOrder:
    def test_xml(self):
        psc1 = decl.ProcStateCodes(1, 'psc1')

        d.session.add(decl.InterfaceEvent(1, psc1, xml='<foo></foo>'))

        assert interface.update_order(1, xml='<bar></bar>') == {
            'id': 1,
            'eventTime': None,
            'partner': None,
            'msgType': None,
            'procEnv': None,
            'procStateDesc': 'psc1',
            'procMsg': None,
            'procResDesc': None,
            'xml': '<bar></bar>',
            }

    def test_resubmit(self):
        d.session.add(decl.ProcStateCodes(1, 'psc1'))
        psc9 = decl.ProcStateCodes(9, 'psc9')

        d.session.add(decl.ErrorCodes(0, 'ec0'))
        ec9 = decl.ErrorCodes(9, 'ec9')

        d.session.add(decl.InterfaceEvent(1, psc9, ec9))

        assert interface.update_order(1, resubmit=True) == {
            'id': 1,
            'eventTime': None,
            'partner': None,
            'msgType': None,
            'procEnv': None,
            'procStateDesc': 'psc1',
            'procMsg': None,
            'procResDesc': 'ec0',
            'xml': None,
            }

    def test_cancel(self):
        psc1 = decl.ProcStateCodes(1, 'psc1')
        d.session.add(decl.ProcStateCodes(9, 'psc9'))

        ec1 = decl.ErrorCodes(1, 'ec1')

        d.session.add(decl.InterfaceEvent(1, psc1, ec1))

        assert interface.update_order(1, cancel=True) == {
            'id': 1,
            'eventTime': None,
            'partner': None,
            'msgType': None,
            'procEnv': None,
            'procStateDesc': 'psc9',
            'procMsg': None,
            'procResDesc': 'ec1',
            'xml': None,
            }
