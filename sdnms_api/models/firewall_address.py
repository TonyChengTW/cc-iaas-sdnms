import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

SAModel = declarative_base()


class FirewallAddressModel(SAModel):
    __tablename__ = 'firewall_address'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    type = sa.Column(sa.String(128), nullable=False)
    content = sa.Column(sa.String(255), nullable=False)
    interface = sa.Column(sa.String(15), nullable=False)
    comment = sa.Column(sa.Text)

    def __init__(self, name, type, content, interface, comment):
        self.name = name
        self.type = type
        self.content = content
        self.interface = interface
        self.comment = comment

    @property
    def as_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'content': self.content,
            'interface': self.interface,
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
