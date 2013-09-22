from brubeck.queryset.base import AbstractQueryset
from schematics.serialize import to_python

class DictQueryset(AbstractQueryset):
    """This class exists as an example of how one could implement a Queryset.
    This model is an in-memory dictionary and uses the model's id as the key.

    The data stored is the result of calling `to_python()` on the model.
    """
    def __init__(self, **kw):
        """Set the db_conn to a dictionary.
        """
        super(DictQueryset, self).__init__(db_conn=dict(), **kw)

    ### Create Functions

    def create_one(self, shield):
        if shield.id in self.db_conn:
            status = self.MSG_UPDATED
        else:
            status = self.MSG_CREATED

        shield_key = str(getattr(shield, self.api_id))
        self.db_conn[shield_key] = to_python(shield)
        return (status, shield)

    def create_many(self, shields):
        statuses = [self.create_one(shield) for shield in shields]
        return statuses

    ### Read Functions

    def read_all(self):
        return [(self.MSG_OK, datum) for datum in self.db_conn.values()]


    def read_one(self, iid):
        iid = str(iid)  # TODO Should be cleaner
        if iid in self.db_conn:
            return (self.MSG_OK, self.db_conn[iid])
        else:
            return (self.MSG_FAILED, iid)

    def read_many(self, ids):
        return [self.read_one(iid) for iid in ids]

    ### Update Functions
    def update_one(self, shield):
        shield_key = str(getattr(shield, self.api_id))
        self.db_conn[shield_key] = to_python(shield)
        return (self.MSG_UPDATED, shield)

    def update_many(self, shields):
        statuses = [self.update_one(shield) for shield in shields]
        return statuses

    ### Destroy Functions

    def destroy_one(self, item_id):
        try:
            datum = self.db_conn[item_id]
            del self.db_conn[item_id]
        except KeyError:
            raise FourOhFourException
        return (self.MSG_UPDATED, datum)

    def destroy_many(self, ids):
        statuses = [self.destroy_one(iid) for iid in ids]
        return statuses

