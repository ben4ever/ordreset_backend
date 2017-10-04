from ordreset import d
from ordreset.db import declarative as decl


def _to_list_of_dicts(rows):
    return [i._asdict() for i in rows]


def get_orders():
    return _to_list_of_dicts(d.session
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


# TODO
def get_order(id_):
    return _to_list_of_dicts(d.session
        .query(
            decl.InterfaceEvent.id_.label('id'),
            decl.InterfaceEvent.xml.label('xml'),
            )
        .filter(decl.InterfaceEvent.id_ == id_)
        .one())


# TODO
def update_order(id_, xml=None, resubmit=False, cancel=False):
    event = (d.session
        .query(decl.InterfaceEvent)
        .filter(decl.InterfaceEvent.id_ == id_)
        .scalar())
    if xml:
        event.xml = xml
    if resubmit:
        event.proc_state_id = 1
        event.proc_result_id = 0
    if cancel:
        event.proc_state_id = 9
    d.session.commit()
