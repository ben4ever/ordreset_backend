from datetime import datetime

from ordreset import d
from ordreset.db import declarative as decl


def _serialize_for_json(dict_):
    for k, v in dict_.items():
        if isinstance(v, datetime):
            dict_[k] = v.isoformat()

    return dict_

def get_orders():
    res = (d.session
        .query(
            decl.InterfaceEvent.id_.label('id'),
            decl.InterfaceEvent.event_date_time.label('eventTime'),
            decl.InterfaceEvent.partner.label('partner'),
            decl.InterfaceEvent.message_type.label('msgType'),
            decl.InterfaceEvent.proc_env.label('procEnv'),
            decl.ProcStateCodes.desc.label('procStateDesc'),
            decl.InterfaceEvent.proc_msg.label('procMsg'),
            decl.ErrorCodes.desc.label('procResDesc'),
            )
        .join(decl.ProcStateCodes)
        .outerjoin(decl.ErrorCodes)
        .order_by('eventTime'))
    return [_serialize_for_json(i._asdict()) for i in res]


def get_order(id_):
    return _serialize_for_json(d.session
        .query(
            decl.InterfaceEvent.id_.label('id'),
            decl.InterfaceEvent.event_date_time.label('eventTime'),
            decl.InterfaceEvent.partner.label('partner'),
            decl.InterfaceEvent.message_type.label('msgType'),
            decl.InterfaceEvent.xml.label('xml'),
            decl.InterfaceEvent.proc_env.label('procEnv'),
            decl.ProcStateCodes.desc.label('procStateDesc'),
            decl.InterfaceEvent.proc_msg.label('procMsg'),
            decl.ErrorCodes.desc.label('procResDesc'),
            )
        .join(decl.ProcStateCodes)
        .outerjoin(decl.ErrorCodes)
        .filter(decl.InterfaceEvent.id_ == id_)
        .one()
        ._asdict())


def update_order(id_, xml=None, resubmit=False, cancel=False):
    event = decl.InterfaceEvent.query.get(id_)
    if xml:
        event.xml = xml
    if resubmit:
        event.proc_state_id = 1
        event.proc_result_id = 0
    if cancel:
        event.proc_state_id = 9
    d.session.commit()

    return get_order(id_)
