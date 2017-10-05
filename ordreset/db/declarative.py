from ordreset import d


class InterfaceEvent(d.Model):
    __tablename__ = 'INTERFACE_event'
    __table_args__ = (
        d.PrimaryKeyConstraint('IntCtrlNo'),
        d.ForeignKeyConstraint(
            ['ProcState'],
            ['BASE_ProcStateCodes.ProcStateCode']),
        d.ForeignKeyConstraint(
            ['ProcResult'],
            ['BASE_ErrorCodes.ErrorCode']),
        )

    id_ = d.Column('IntCtrlNo', d.Integer)

    event_date_time = d.Column('EventDateTime', d.DateTime)
    partner = d.Column('PartnerId', d.Text)
    message_type = d.Column('Message_Type', d.Text)
    xml = d.Column('Payload', d.Text)
    proc_env = d.Column('ProcEnv', d.Text)
    proc_state_id = d.Column('ProcState', d.Integer)
    proc_msg = d.Column('ProcMessage', d.Text)
    proc_result_id = d.Column('ProcResult', d.Integer)

    proc_state = d.relationship('ProcStateCodes')
    proc_result = d.relationship('ErrorCodes')

    def __init__(self, id_, proc_state=None, proc_result=None,
            event_date_time=None, partner=None, message_type=None, xml=None,
            proc_env=None, proc_msg=None):
        self.id_ = id_
        self.proc_state = proc_state
        self.proc_result = proc_result
        self.event_date_time = event_date_time
        self.partner = partner
        self.message_type = message_type
        self.xml = xml
        self.proc_env = proc_env
        self.proc_msg = proc_msg


class ProcStateCodes(d.Model):
    __tablename__ = 'BASE_ProcStateCodes'
    __table_args__ = (
        d.PrimaryKeyConstraint('ProcStateCode'),
        )

    id_ = d.Column('ProcStateCode', d.Integer)
    desc = d.Column('ProcStateDesc', d.Text)

    def __init__(self, id_, desc=None):
        self.id_ = id_
        self.desc = desc


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

    def __init__(self, id_, desc=None):
        self.id_ = id_
        self.desc = desc
