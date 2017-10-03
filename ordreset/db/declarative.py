from ordreset import d


class InterfaceEvent(d.Model):
    __tablename__ = 'INTERFACE_event'
    __table_args__ = (
        d.PrimaryKeyConstraint('IntCtrlNo'),
        d.ForeignKeyConstraint(
            ['ProcState', 'ProcResult'],
            ['BASE_ProcStateCodes.ProcStateCode', 'BASE_ErrorCodes.pa_partner',
             'order_str.oh_order', 'order_str.os_store_loc']),
        )

    id_ = d.Column('IntCtrlNo', d.Integer)

    event_date_time = d.Column('EventDateTime', d.DateTime)
    partner = d.Column('PartnerId', d.Text)
    message_type = d.Column('Message_Type', d.Text)
    proc_state_id = d.Column('ProcState', d.Integer)
    proc_result_id = d.Column('ProcResult', d.Integer)
    proc_msg = d.Column('ProcMessage', d.Text)
    proc_env = d.Column('ProcEnv', d.Text)

    proc_state = d.relationship('ProcStateCodes')
    proc_result = d.relationship('ErrorCodes')

    def __init__(self, id_, event_date_time=None, partner=None,
            message_type=None, ):
        self.id_ = id_
        self.name = name


class ProcStateCodes(d.Model):
    __tablename__ = 'BASE_ProcStateCodes'
    __table_args__ = (
        d.PrimaryKeyConstraint('ProcStateCode'),
        )

    id_ = d.Column('ProcStateCode', d.Integer)
    desc = d.Column('ProcStateDesc', d.Text)

    def __init__(self, entity, partner, order_id, status=None,
                 date_amended=None, date_created=None):
        self.entity = entity
        self.partner = partner
        self.order_id = order_id
        self.status = status
        self.date_amended = date_amended
        self.date_created = date_created


class ErrorCodes(d.Model):
    __tablename__ = 'BASE_ErrorCodes'
    __table_args__ = (
        d.PrimaryKeyConstraint('ErrorCode'),
        )

    # In the underlying DB this is actually declared as data type ``Text``
    # since Kane set it up that way. I however, use ``Integer`` here for
    # consistency to the tables referencing this column.
    id_ = d.Column('ErrorCode', d.Integer)
    desc = d.Column('ErrorDesc', d.Text)

    def __init__(self, order_header, store_loc, status=None, sys_id=None):
        self.order_header = order_header
        self.store_loc = store_loc
        self.status = status
        self.sys_id = sys_id
