import phylib;
import os;
import sqlite3;
import math;
################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;
FRAME_INTERVAL = 0.01

# add more here

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;
    
    def svg(self):
       
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
      
        

class RollingBall(phylib.phylib_object):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number, position (x, y), and velocity (vx, vy) as arguments.
        """
  
        phylib.phylib_object.__init__( self,
                                       phylib.PHYLIB_ROLLING_BALL,
                                       number,
                                       pos, vel,acc, 
                                       0.0, 0.0 );
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;

    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])

        


class Hole(phylib.phylib_object):
    """
    Python Hole class.
    """

    def __init__(self,pos):
        """
        Constructor function. Requires hole number and position (x, y) as arguments.
        """
        # Directly call the superclass' __init__ method
        phylib.phylib_object.__init__( self,
                                       phylib.PHYLIB_HOLE,
                                       0,
                                       pos, None, None,
                                       0.0, 0.0);

        # this converts the phylib_object into a Hole class
        self.__class__ = Hole;

    def svg(self):
        
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)

class HCushion(phylib.phylib_object):
    """
    Python Horizontal Cushion class.
    """

    def __init__(self, y):
        """
        Constructor function. Requires cushion number and position (x, y) as arguments.
        """

        
        # Directly call the superclass' __init__ method
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HCUSHION,
                                      0,
                                      None, None, None,
                                      0.0,y);
        
        # this converts the phylib_object into an HCushion class
        self.__class__ = HCushion;


    def svg(self):
        y = -25 if self.obj.hcushion.y == 0 else 2700
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (y)



        

class VCushion(phylib.phylib_object):
    """
    Python Vertical Cushion class.
    """

    def __init__(self, x):
        """
        Constructor function. Requires cushion number and position (x, y) as arguments.
        """
        # Directly call the superclass' __init__ method
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_VCUSHION,
                                      0,
                                      None, None, None,
                                      x, 0.0 );

        # this converts the phylib_object into a VCushion class
        self.__class__ = VCushion;

    def svg(self):
        x = -25 if self.obj.vcushion.x == 0 else 1350
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x)


    




################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # adding svg method
    def svg(self):
        svg_content = HEADER
        for obj in self:
            if obj is not None:
                svg_content += obj.svg()
        svg_content += FOOTER
        return svg_content


    # helper method given through courselink
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                Coordinate(0,0),
                Coordinate(0,0),
                Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                Coordinate( ball.obj.still_ball.pos.x,
                ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    #helper method
    def cueBall(self):
    
        # looping through balls in table
        for ball in self:
            if ball.type == phylib.PHYLIB_STILL_BALL:   # check if still
                if ball.obj.still_ball.number == 0:
                    return ball
            elif ball.type == phylib.PHYLIB_ROLLING_BALL: # check if rolling
                if ball.obj.rolling_ball.number == 0:
                    print("Found cue ball.")
                    return ball
        return None # none if its not rolling or stil

    def addBalls(self):

        coordinates = [
                Coordinate(675, 2025), # Cue Ball (White) 0
                Coordinate(675, 675),  # Yellow 1
                Coordinate(645, 622),  # Blue 2
                Coordinate(614, 569),  # Red 3
                Coordinate(584, 516),  # Purple 4
                Coordinate(797, 463),  # Orange 5
                Coordinate(614, 463),  # Green   6
                Coordinate(706, 516),  # Brown 7
                Coordinate(675, 569),  # Black  8
                Coordinate(706, 622),  # Light Yellow 9
                Coordinate(736, 569),  # Light Blue 10
                Coordinate(767, 516),  # Pink 11
                Coordinate(553, 463),  # Medium Purple 12
                Coordinate(736, 463),  # Light Salmon 13
                Coordinate(645, 516),  # Light Green 14
                Coordinate(675, 463),  # Sandy Brown 15
                ]

        for i in range(len(coordinates)):
            self += StillBall(i, coordinates[i])
        
        # for ball in self:
        #     print(type(ball))
        return self
        

    
    

class Database():
    
    # initailizes the database connection
    def __init__(self, reset=False):
        if reset == True:
            if os.path.exists("phylib.db"):
                os.remove("phylib.db")
        self.conn = sqlite3.connect("phylib.db")

    
    # creating the tables 
    def createDB(self):

        cur = self.conn.cursor()

        cur.execute( """CREATE TABLE IF NOT EXISTS Ball 
                 ( BALLID  INTEGER PRIMARY KEY AUTOINCREMENT,
                   BALLNO  INTEGER NOT NULL,
                   XPOS    FLOAT   NOT NULL,
                   YPOS    FLOAT   NOT NULL,
                   XVEL    FLOAT,
                   YVEL    FLOAT ); """ ) 

        cur.execute( """CREATE TABLE IF NOT EXISTS TTABLE 
                 ( TABLEID INTEGER PRIMARY KEY AUTOINCREMENT,
                   TIME    FLOAT   NOT NULL
                    ); """ )

        cur.execute( """CREATE TABLE IF NOT EXISTS BallTable 
                 ( BALLID  INTEGER NOT NULL,
                   TABLEID INTEGER NOT NULL,
                   FOREIGN KEY (BALLID) REFERENCES BALL(BALLID),
                   FOREIGN KEY (TABLEID) REFERENCES TTABLE(TABLEID) 
                   ); """ )

        cur.execute( """CREATE TABLE IF NOT EXISTS Shot
                  ( SHOTID INTEGER PRIMARY KEY AUTOINCREMENT,
                    PLAYERID INTEGER NOT NULL,
                    GAMEID INTEGER NOT NULL,
                    FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                    FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
                    ); """)

         


        cur.execute( """CREATE TABLE IF NOT EXISTS TableShot
                 ( TABLEID INTEGER NOT NULL,
                   SHOTID  INTEGER NOT NULL,
                   FOREIGN KEY (TABLEID) REFERENCES TTABLE(TABLEID),
                   FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
                   ); """ )

        cur.execute( """CREATE TABLE IF NOT EXISTS Game
                 ( GAMEID INTEGER PRIMARY KEY AUTOINCREMENT,
                   GAMENAME VARCHAR(64) NOT NULL
                   
                   ); """ )

        cur.execute( """CREATE TABLE IF NOT EXISTS Player
                 ( PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT,
                   GAMEID   INTEGER NOT NULL,
                   PLAYERNAME VARCHAR(64) NOT NULL,
                   FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
                   ); """ )

        cur.close()
        self.conn.commit()


    # reads the state of the table by its specfic ID
    def readTable(self, tableID):
        # creating instance of table and populating
        populateTable = Table()

        # database cursor
        cur = self.conn.cursor()

        # error check to see if a table with a certain ID exists
        cur.execute("SELECT COUNT(*) FROM TTable WHERE TABLEID = ?", (tableID + 1,))
        if cur.fetchone()[0] == 0:
            cur.close()
            return None  # None is returned if condition passes

        # This will fetch the data of the ball
        cur.execute("""
            SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL 
            FROM Ball 
            JOIN BallTable ON Ball.BALLID = BallTable.BALLID 
            WHERE BallTable.TABLEID = ?
        """, (tableID + 1,))
        rows = cur.fetchall()

        # iterate through each row
        for row in rows:
            # Extracting the velocity components
            xvel = row[4] if row[4] is not None else 0
            yvel = row[5] if row[5] is not None else 0

        # Checking if both xvel and yvel are zero to avoid division by zero
            if xvel == 0 and yvel == 0:
                ball = StillBall(row[1], Coordinate(row[2], row[3]))
            else:
                velocity = Coordinate(xvel, yvel)
                velSpeed = phylib.phylib_length(velocity)

            # Ensure velSpeed is not zero before dividing
                if velSpeed > 0:
                    direction = Coordinate((xvel * -1.0) / velSpeed, (yvel * -1.0) / velSpeed)
                else:
                    direction = Coordinate(0, 0)

                # Adjusted for DRAG, if necessary
                dragEffect = Coordinate(direction.x * DRAG, direction.y * DRAG)
                ball = RollingBall(row[1], Coordinate(row[2], row[3]), velocity, dragEffect)

            populateTable += ball  # this will add it to the table

        # this will add the time to table
        cur.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (tableID + 1,))
        tableTime = cur.fetchone()[0]
        populateTable.time = tableTime

        cur.close() 
    # Removed self.conn.commit() since this function is not intended to modify the database

        return populateTable  # Return the populated table

        




    # saves current state of the pool table 
    def writeTable(self, table):
        
        cur = self.conn.cursor()

        # this will insert the current simulation time into TTABLE and get ID
        cur.execute("INSERT INTO TTable (TIME) VALUES (?)", (table.time,))
        table_id = cur.lastrowid # IDS linked to table state 

        # looping through all ball objects in table
        for obj in table:  
            
            # if still ball 
            if isinstance(obj, StillBall):
            
                # dont need velocity since still
                ball_number = obj.obj.still_ball.number
                pos_x = obj.obj.still_ball.pos.x
                pos_y = obj.obj.still_ball.pos.y
                
                # puts still ball into the ball table
                cur.execute(
                "INSERT INTO Ball (BALLNO, XPOS, YPOS) VALUES (?, ?, ?)",
                (ball_number, pos_x, pos_y)
                )

                ball_id = cur.lastrowid # ID retrived 

                # links the ball to the table
                cur.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ball_id, table_id))
                
            # if its a rollling ball
            elif isinstance(obj, RollingBall):
                # attributes for rolling ball including velocity
                ball_number = obj.obj.rolling_ball.number
                pos_x = obj.obj.rolling_ball.pos.x
                pos_y = obj.obj.rolling_ball.pos.y
                vel_x = obj.obj.rolling_ball.vel.x
                vel_y = obj.obj.rolling_ball.vel.y

                # put the rolling ball in the table
                cur.execute(
                "INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)",
                (ball_number, pos_x, pos_y, vel_x, vel_y)
                )
            
           
            
                ball_id = cur.lastrowid # ID retireved 

                # Link ball to the table
                cur.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)", (ball_id, table_id))



        self.conn.commit()
        cur.close()

        return table_id - 1  # accomadating for indexing
    
    def close(self):
        self.conn.commit()
        self.conn.close()


    def countTables(self):
        """
        Counts the number of table states in the database.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM TTable")
        count = cur.fetchone()[0]  # Fetches the first column of the first (and only) row.
        cur.close()
        return count


    # helper method used to retrive info for players for a given gameID
    def getGame(self, gameID):
        
        # manages the cursor
        with self.conn.cursor() as cur:
            # SQL query that gets game and player info
            cur.execute("""
                SELECT Player.PLAYERID, Game.GAMENAME, Player.PLAYERNAME
                FROM Game
                INNER JOIN Player ON Game.GAMEID = Player.GAMEID
                WHERE Game.GAMEID = ?;
            """, (gameID + 1,))
            result = cur.fetchall()  # gets all rows for the query
    
        return result
       

    # helper method creates new game entry in game table
    def setGame(self, gameName, player1Name, player2Name):
        
        cur = self.conn.cursor()

        # inserts new game into table 
        cur.execute(""" INSERT INTO Game (GAMENAME) VALUES (?) """, (gameName,))
        self.gameID = cur.lastrowid  

        # inserting player1 in
        cur.execute("""
            INSERT INTO Player (GAMEID, PLAYERNAME)
            VALUES (?, ?)
        """, (self.gameID, player1Name))
    
        # insert player2 in
        cur.execute("""
            INSERT INTO Player (GAMEID, PLAYERNAME)
            VALUES (?, ?)
        """, (self.gameID, player2Name))
    
        self.conn.commit()
    
   
    # helper method that inserts records of the table state 
    def TableShot(self, tableID, shotID):
        
        # making sure connection is good
        with self.conn as conn:  
            
            cur = conn.cursor()
            # inserts tableID and shotID into the table
            cur.execute("""
                INSERT INTO TableShot (TABLEID, SHOTID) 
                VALUES (?, ?);
            """, (tableID, shotID))
    
    
    # helper method creates new shot entry in the shot table
    def newShot(self, playerName, table, xvel, yvel, gameID):

        cur = self.conn.cursor()
    
        # gets the player's ID 
        playerGame = cur.execute("SELECT PLAYERID, GAMEID FROM Player WHERE PLAYERNAME = ? AND GAMEID = ?",
                                 (playerName, self.gameID)).fetchone()
      
        if playerGame:
           
            # inserts new shot record 
            cur.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ? )",
                        (playerGame[0], self.gameID))
            shotId = cur.lastrowid
       
        else:
            
            shotId = None # if no matching player is found

        cur.close()
        self.conn.commit()
    
        # Assuming shotId is None if playerGame fetch failed
        return shotId if shotId is not None else None



class Game():

    
    # initializes a new game instance 
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        
        self.database = Database()  # data connection

        # loads existing game based off his ID
        if isinstance(gameID, int):  
            if any([gameName, player1Name, player2Name]):  
                
                # raise an error if other parameters are given
                raise TypeError("When gameID is set, gameName, player1Name, and player2Name must be None.")
            self.gameID = gameID
            db = self.database.getGame(gameID + 1)  # fetches game details

            if not db:
                # if no game matches raise an error
                raise ValueError("No game found with the specified gameID.")

            # extracts game details
            self.gameName, self.player1Name, self.player2Name = db[0][1], db[0][2], db[1][2]
            
        # creates new game entry
        elif gameID is None and all(isinstance(name, str) for name in [gameName, player1Name, player2Name]):
            
            # setting atrribiutes directly
            self.gameName, self.player1Name, self.player2Name = gameName, player1Name, player2Name

            # create new game in database 
            self.gameID = self.database.setGame(gameName, player1Name, player2Name)
            
        else:
            # Handle invalid arguments
            raise TypeError("Invalid input.")


    # attempted stuff that doesn't work
    
    #checks if the players have been assigned to their groups. If not, it does so based on the first successful potted ball.
    def process_shot(self, potted_balls):
        if not self.player1_group and not self.player2_group:  # No groups assigned yet
            for ball in potted_balls:
                if 1 <= ball <= 7:
                    self.player1_group = 'low' if self.current_player == self.player1 else 'high'
                    self.player2_group = 'high' if self.player1_group == 'low' else 'low'
                    break
                elif 9 <= ball <= 15:
                    self.player1_group = 'high' if self.current_player == self.player1 else 'low'
                    self.player2_group = 'low' if self.player1_group == 'high' else 'high'
                    break
        
        if foul or not self.potted_correct_ball(potted_balls):
            self.switch_player()

        # Code to handle continuation of turns, switching players, etc.

    def potted_correct_ball(self, potted_balls):
        if not potted_balls:
            return False  # No ball was potted

        player_group = self.player1_group if self.current_player == self.player1 else self.player2_group
        ball_range = range(1, 8) if player_group == 'low' else range(9, 16)

        return any(ball in ball_range for ball in potted_balls)


    def switch_player(self):
        self.current_player, self.other_player = self.other_player, self.current_player

    
    # stimulates shooting cue ball on a pool table
    def shoot(self, gameName, playerName, table, xvel, yvel):
        
        # record the shot in database
        shotID = self.database.newShot(playerName, table, xvel, yvel, self.gameID)
   
        # error handling
        if shotID is None:
            raise Exception("No shotID sorry.")

        #print(cueBall)
        # Find the cue ball in the table
        Ballcue = table.cueBall()
     
        if not Ballcue:
            raise Exception("No cueball sorry.") # error handling

        print(Ballcue)
        
        

        # this will store curr position of whiteball aka cue ball
        xpos, ypos = Ballcue.obj.still_ball.pos.x, Ballcue.obj.still_ball.pos.y

       
        # set cue balls state to rolling and setting velo and pos
        Ballcue.type = phylib.PHYLIB_ROLLING_BALL
        Ballcue.obj.rolling_ball.number = 0
        Ballcue.obj.rolling_ball.pos.x = xpos
        Ballcue.obj.rolling_ball.pos.y = ypos
        Ballcue.obj.rolling_ball.vel.x = xvel
        Ballcue.obj.rolling_ball.vel.y = yvel

        # Calculate accel
        speed = phylib.phylib_length(Ballcue.obj.rolling_ball.vel)

        if speed > VEL_EPSILON:

            Ballcue.obj.rolling_ball.acc.x = (-xvel / speed) * DRAG
            Ballcue.obj.rolling_ball.acc.y = (-yvel / speed) * DRAG

        # Simulate the shots effects on table 
        
        svg_frames = []
        while table:

            Starttime = table.time
            table = table.segment()

            if table is not None:

                EndTime = table.time

            Finaltime = EndTime - Starttime
            Finaltime = int(Finaltime/FRAME_INTERVAL)

            for frame in range(Finaltime):
                
                Newtable = table.roll(frame * FRAME_INTERVAL)
                Newtable.time = Starttime + (frame * FRAME_INTERVAL)
                
                svg_frames.append(Newtable.svg())


                # Save updated table to database for frame
                tableID = self.database.writeTable(Newtable)
                print(tableID)

                # linking recorded table state with shotID
                self.database.TableShot(tableID, shotID)

            
            
            else:
                break;
         
            table = segment    
        
        return svg_frames


