import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

SAModel = declarative_base()


class FirewallServiceModel(SAModel):
    __tablename__ = 'firewall_service'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    protocol_type = sa.Column(sa.String(15), nullable=False)
    address = sa.Column(sa.String(128))
    dest_port = sa.Column(sa.String(30))
    dest_port_low = sa.Column(sa.Integer)
    dest_port_high = sa.Column(sa.Integer)
    type = sa.Column(sa.String(128))
    code = sa.Column(sa.String(128))
    protocol_number = sa.Column(sa.String(128))
    comment = sa.Column(sa.Text)

    def __init__(self, name, protocol_type, address, dest_port, dest_port_low, dest_port_high,
                 type, code, protocol_number, comment):
        self.name = name
        self.protocol_type = protocol_type
        self.address = address
        self.dest_port = dest_port
        self.dest_port_low = dest_port_low
        self.dest_port_high = dest_port_high
        self.type = type
        self.code = code
        self.protocol_number = protocol_number
        self.comment = comment

    @property
    def as_dict(self):
        return {
            'name': self.name,
            'protocol_type': self.protocol_type,
            'address': self.address,
            'dest_port': self.dest_port,
            'dest_port_low': self.dest_port_low,
            'dest_port_high': self.dest_port_high,
            'type': self.type,
            'code': self.code,
            'protocol_number': self.protocol_number,
            'comment': self.comment
        }

    def save(self, session):
        with session.begin():
            session.add(self)

    @classmethod
    def get_list(cls, session):
        models = []

        with session.begin():
            query = session.query(cls)
            models = query.all()

        return models
