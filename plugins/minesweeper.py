"""
The MIT License (MIT)

Copyright (c) 2024 Mikk155

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from plugins.main import *

class MineSweper:

    columns = 10;

    def __init__( self, num_bombas: int, blocks: int, objetive_emote: str ):

        # Cap bombs to have space for the emote
        if num_bombas > ( blocks * self.columns ) - 1:
            num_bombas = ( blocks * self.columns ) - 1;

        if not self.is_emote( objetive_emote ):
            objetive_emote = '<:walter:808255870113939477>';

        total_slots = ( blocks * self.columns ) - num_bombas - 1;
        bombas = [ ":bomb:" for _ in range( num_bombas ) ];
        slots = [ ":o:" for _ in range( total_slots ) ];

        slots.append( objetive_emote );
        self.emoji = objetive_emote;

        tablero = bombas + slots
        random.shuffle( tablero );

        self.columnas = [];

        for i in range(blocks):
            line = tablero[ i * self.columns:(i + 1) * self.columns ]

            for ei, emote in enumerate( line ):

                line[ ei ] = self.increase_count( ( ei < 9 and line[ ei + 1 ] == ':bomb:' ), ei, line );
                line[ ei ] = self.increase_count( ( ei > 0 and line[ ei - 1 ] == ':bomb:' ), ei, line );
            
                if i < blocks - 1:
                    next_line = tablero[ ( i + 1 ) * self.columns:( ( i + 1 ) + 1 ) * self.columns ]
                    line[ ei ] = self.increase_count( ( next_line[ ei ] == ':bomb:' ), ei, line );
                    line[ ei ] = self.increase_count( ( ei > 0 and next_line[ ei - 1 ] == ':bomb:' ), ei, line );
                    line[ ei ] = self.increase_count( ( ei < 9 and next_line[ ei + 1 ] == ':bomb:' ), ei, line );
                if i > 0:
                    prev_line = tablero[ ( i - 1 ) * self.columns:( ( i - 1 ) + 1 ) * self.columns ]
                    line[ ei ] = self.increase_count( ( prev_line[ ei ] == ':bomb:' ), ei, line );
                    line[ ei ] = self.increase_count( ( ei > 0 and prev_line[ ei - 1 ] == ':bomb:' ), ei, line );
                    line[ ei ] = self.increase_count( ( ei < 9 and prev_line[ ei + 1 ] == ':bomb:' ), ei, line );

            for number, reg in gpUtils.emote_number().items():
                while number in line:
                    line[ line.index( number ) ] = f':{reg}:';

            self.columnas.append( "".join( [ f"||{emote}||" for emote in line ] ) )

    def increase_count( self, condition: bool, index : int, line : list ):
        return self.increase( line[ index ] ) if condition else line [ index ];
        
    def is_emote( self, emote: str ):
        return ( ( emote[0] == ':' and emote.endswith( ':' ) ) or ( emote[0] == '<' and emote.endswith( '>' ) ) );

    def increase( self, string: str ):
        return string if string in [ self.emoji, ':bomb:' ] else str( int( string ) + 1 ) if string.isnumeric() else '1';

    def message( self ):
        message = '';
        for line in self.columnas:
            message += line + '\n';
        return message;

@bot.tree.command()
@app_commands.describe(
    bombs='Number of bombs',
    blocks='Number of blocks',
    emoji='Objetive emoji',
)
async def minesweeper( interaction: discord.Interaction, bombs: int = 6, blocks: int = 4, emoji:str = '<:walter:808255870113939477>' ):
    """Mine sweeper minigame"""

    try:

        minesweper = MineSweper( bombs, blocks, emoji );

        await interaction.response.send_message( minesweper.message() );

    except Exception as e:

        await interaction.response.send_message( "Exception: {}".format( e ) );
