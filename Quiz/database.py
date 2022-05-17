# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql://uzx1vchtsyougsr0:LVM3RgExwaD1d9BS6f5Z@bdlrufaxbcny5wemkm9v-mysql.services.clever-cloud.com:3306/bdlrufaxbcny5wemkm9v"
# # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

from mysql.connector import connection


# Dependency
def get_db():
    try:
        # conn = connection.MySQLConnection(user = 'uzx1vchtsyougsr0',
        #                       host = 'bdlrufaxbcny5wemkm9v-mysql.services.clever-cloud.com',
        #                       password ="LVM3RgExwaD1d9BS6f5Z",
        #                       database = 'bdlrufaxbcny5wemkm9v')

        # mysql://ucxyhsylomewrmo3:Wr6na6NCTOcb8WDGlcrv@b1tsjmitzrdsyeos5twj-mysql.services.clever-cloud.com:3306/b1tsjmitzrdsyeos5twj
        conn = connection.MySQLConnection(user = 'ucxyhsylomewrmo3',
                              host = 'b1tsjmitzrdsyeos5twj-mysql.services.clever-cloud.com',
                              password ="Wr6na6NCTOcb8WDGlcrv",
                              database = 'b1tsjmitzrdsyeos5twj')
        return conn
    except(Exception):
        # conn.close()
        pass

def close_db(conn):
    conn.close()