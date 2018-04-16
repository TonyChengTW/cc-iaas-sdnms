import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

SAModel = declarative_base()


class FirewallPolicyModel(SAModel):
    __tablename__ = 'firewall_policy'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    incoming_interface = sa.Column(sa.String(15), nullable=False)
    outgoing_interface = sa.Column(sa.String(15), nullable=False)
    source = sa.Column()
    destination = sa.Column()
    schedule = sa.Column(sa.String(128))
    services = sa.Column()
    action = sa.Column(sa.String(30))
    nat = sa.Column(sa.String(30))
    comment = sa.Column(sa.Text)
    status = sa.Column(sa.String(30))

    def __init__(self, name, incoming_interface, outgoing_interface, source, destination, schedule,
                 services, action, nat, comment, status):
        self.name = name
        self.incoming_interface = incoming_interface
        self.outgoing_interface = outgoing_interface
        self.source = source
        self.destination = destination
        self.schedule = schedule
        self.services = services
        self.action = action
        self.nat = nat
        self.comment = comment
        self.status = status

    @property
    def as_dict(self):
        return {
            'name': self.name,
            'incoming_interface': self.incoming_interface,
            'outgoing_interface': self.outgoing_interface,
            'source': self.source,
            'destination': self.destination,
            'schedule': self.schedule,
            'services': self.services,
            'action': self.action,
            'nat': self.nat,
            'comment': self.comment,
            'status': self.status
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
