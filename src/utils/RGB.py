class RGB:

    R = 0;
    G = 0;
    B = 0;

    def __init__( self, Red: int = 0, Green: int = 0, Blue: int = 0 ) -> None:
        self.R: int = max( 0, min( 255, Red ) );
        self.G: int = max( 0, min( 255, Green ) );
        self.B: int = max( 0, min( 255, Blue ) );

    def __repr__( self ):
        return "#{:02x}{:02x}{:02x}".format( self.R, self.G, self.B )

    @property
    def hex( self ) -> int:
        return ( self.R << 16 ) | ( self.G << 8 ) | self.B;
