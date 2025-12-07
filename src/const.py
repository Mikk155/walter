import discord;
from enum import IntEnum;
from src.utils.RGB import RGB;

MikkID: int = 744768007892500481;

class LimitlessPotential:

    id: int = 744769532513615922;

    class Channels( IntEnum ):
        Announcements: int = 842129545494134785;
        Users: int = 1343203830787080203;
        BotLogs: int = 1343209173969535108;
        GreetTheGafther: int = 1376757390757724298;
        Trusted: int = 1343197825751715851;
        DiscordLogs: int = 1343203478742241372;
        BetaTesting: int = 1403853307629277194;
        CountTogether: int = 1343206179878211755;
        LPMemes: int = 1343244435583926323;

    Invites: dict[ str, int ] = {};

class TheCult:

    id: int = 1216162825307820042;

    class Channels( IntEnum ):
        Announcements: int = 1397367866667434125;
        Benefactors: int = 1216208600725196922;
        Users: int = 1447021578532425802;
        DiscordLogs: int = 1397355050715578439;

    Invites: dict[ str, int ] = {};

class Colors( IntEnum ):
    LimitlessPotential: int = RGB( 200, 0, 200 ).hex;
    TheCult: int = RGB( 200, 0, 50 ).hex;
