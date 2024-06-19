import psycopg2
from consts import Consts
from contextlib import closing
from profile import Profile

class PostgresDB:
    def __init__(self):
        self.conn = psycopg2.connect(Consts.DATABASE_URL, sslmode='require')

    def Reconnect(self):
        self.conn = psycopg2.connect(Consts.DATABASE_URL, sslmode='require')
        
    def GetProfile(self, userId):
        cursor = None
        try:
            sql = f"SELECT UserID, Main, Secondaries, Rank, FriendCode, GameplayType FROM Profiles WHERE UserID = \'{userId}\'"
            cursor = self.conn.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            if(row != None):
                return Profile(row[0], row[1], row[2], row[3], row[4], row[5])
            else:
                return None
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            if cursor is not None:
                cursor.close()            
            return None

    def UpsertProfile(self, userId, main, secondaries, rank, friendCode, gameplayType):
        cursor = None
        try:
            doesProfileExist = self.GetProfile(userId)

            if(doesProfileExist is None):
                sql = f"INSERT INTO Profiles(UserID, Main, Secondaries, Rank, FriendCode, GameplayType) VALUES (\'{userId}\', \'{main}\', \'{secondaries}\', \'{rank}\', \'{friendCode}\',\'{gameplayType}\')"
            else:
                if(main is not None):
                    doesProfileExist.Main = main
                if(secondaries != "{}"):                          
                    secondariesInsertValue = secondaries
                elif(secondaries == "{}"):                    
                    if(doesProfileExist.Secondaries != "[]"):
                        secondariesSplitString = ''.join(str(f"{item.strip()},") for item in doesProfileExist.Secondaries)
                        secondariesInsertValue = "{"+secondariesSplitString[:-1]+"}"
                    else:
                        secondariesInsertValue = "{}"      
                if(friendCode is not None):
                    doesProfileExist.FriendCode = friendCode
                if(gameplayType is not None):
                    doesProfileExist.GameplayType = gameplayType
                if(rank is not None):
                    doesProfileExist.Rank = rank
                
                sql = f"UPDATE Profiles SET Main = \'{doesProfileExist.Main}\', Secondaries = \'{secondariesInsertValue}\', Rank = \'{doesProfileExist.Rank}\', FriendCode = \'{doesProfileExist.FriendCode}\', GameplayType = \'{doesProfileExist.GameplayType}\' WHERE UserID = \'{userId}\'"
            cursor = self.conn.cursor()
            cursor.execute(sql) 
            self.conn.commit()
            return True
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            if cursor is not None:
                cursor.rollback()            
            return None
        finally:
            if cursor is not None:
                cursor.close()

    def DeleteProfile(self, userId):
        cursor = None
        try:
            sql = f"DELETE FROM Profiles WHERE UserID = \'{userId}\'"
            cursor = self.conn.cursor()
            cursor.execute(sql) 
            self.conn.commit()
            return True
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            if cursor is not None:
                cursor.close()            
            return None
    