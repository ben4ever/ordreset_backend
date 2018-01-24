from datetime import datetime
import json

import pytest

from ordreset import d
from ordreset.db import declarative as decl, interface


@pytest.fixture
def call_and_unpack(client):
    def call(url):
        return json.loads(client.get(url).get_data().decode())

    return call


def test_get_orders(call_and_unpack):
    psc1 = decl.ProcStateCodes(1, 'psc1')
    psc2 = decl.ProcStateCodes(2, 'psc2')

    ec1 = decl.ErrorCodes(11, 'ec1')
    ec2 = decl.ErrorCodes(12, 'ec2')

    d.session.add(decl.InterfaceEvent(1, psc1, ec1))
    d.session.add(decl.InterfaceEvent(2, psc2, ec2))

    assert call_and_unpack('/orders') == [
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
        ]


def test_get_order(call_and_unpack):
    psc1 = decl.ProcStateCodes(1, 'psc1')

    ec1 = decl.ErrorCodes(11, 'ec1')

    d.session.add(decl.InterfaceEvent(
        1, psc1, ec1, datetime(2017, 1, 1), 'partner1',
        'msgtype1', '<foo></foo>', 'PROD', 'errmsg1'))

    assert call_and_unpack('/orders/1') == {
            'id': 1,
            'eventTime': '2017-01-01T00:00:00',
            'partner': 'partner1',
            'msgType': 'msgtype1',
            'xml': '<foo></foo>',
            'procEnv': 'PROD',
            'procStateDesc': 'psc1',
            'procMsg': 'errmsg1',
            'procResDesc': 'ec1',
        }


class TestUpdateOrder:
    def test_xml(self, client):
        psc1 = decl.ProcStateCodes(1, 'psc1')

        d.session.add(decl.InterfaceEvent(1, psc1, xml='<foo></foo>'))

        resp = client.post(
            '/orders/1',
            data=json.dumps(
                {'xml': '<bar></bar>'},
                indent=2,
                sort_keys=True
                ),
            content_type='application/json',
            )

        assert json.loads(resp.get_data().decode()) == {
                'id': 1,
                'eventTime': None,
                'partner': None,
                'msgType': None,
                'xml': '<bar></bar>',
                'procEnv': None,
                'procStateDesc': 'psc1',
                'procMsg': None,
                'procResDesc': None,
            }

    def test_cancel(self, client):
        d.session.add(decl.ProcStateCodes(9, 'psc9'))

        d.session.add(decl.InterfaceEvent(1))

        resp = client.post(
            '/orders/1',
            data=json.dumps(
                {'cancel': True},
                indent=2,
                sort_keys=True
                ),
            content_type='application/json',
            )

        assert json.loads(resp.get_data().decode()) == {
                'id': 1,
                'eventTime': None,
                'partner': None,
                'msgType': None,
                'xml': None,
                'procEnv': None,
                'procStateDesc': 'psc9',
                'procMsg': None,
                'procResDesc': None,
            }

    def test_no_action(self, client):
        d.session.add(decl.InterfaceEvent(1))

        with pytest.raises(interface.NoActionError):
            client.post(
                '/orders/1',
                data=json.dumps(
                    {'foo': True},
                    indent=2,
                    sort_keys=True
                    ),
                content_type='application/json',
                )
