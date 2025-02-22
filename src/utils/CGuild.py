from __main__ import developer;

class CGuild:

    @property
    def Owner(self) -> int:
        '''Mikk ID'''
        return 744768007892500481;

    @property
    def TestServer(self) -> int:
        '''Test server ID'''
        return 1145236064596918304;

    @property
    def LimitlessPotential(self) -> int:
        '''Limitless potential server ID'''
        return 744769532513615922 if not developer else self.TestServer;

    @property
    def TheCult(self) -> int:
        '''The Cult server ID'''
        return 1216162825307820042 if not developer else self.TestServer;

    @property
    def Channel_Welcome(self) -> int:
        return 1118352656096829530 if not developer else 1342674343003422800;

    @property
    def Channel_Users(self) -> int:
        return 842174687445778483 if not developer else 1342794342783254661;
