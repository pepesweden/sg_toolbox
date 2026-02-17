import logging
import psycopg2
from psycopg2 import pool 
import bcrypt

logger = logging.getLogger(__name__)

class AuthManager:
    # saves database URL to variable
    def __init__(self, database_url):
        self.database_url = database_url

        # Create database connection pool
        self.connection_pool = pool.SimpleConnectionPool(
            minconn=1,      # Min 1 connection always open
            maxconn=10,     # Max 10 concurrent conns
            dsn=database_url
        )

        self.init_db()                    # create database at start
        self.create_default_admin()       # Create admin user


    # Method to create 
    def init_db(self):
        try:
            # conn = psycopg2.connect(self.database_url) #<- Intividual connetion by user 
            conn = self.connection_pool.getconn() #Use connection pooling

        except Exception as e:
            logger.error(f" ❌ Failed to get database connection: {e}")
            return None  # Retur None = "login failed"

        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(50) PRIMARY KEY,
                    password_hash BYTEA NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                )
            ''')
            conn.commit()

        #Catch database error (corruption, syntax error etc.)
        except Exception as e:
            logger.error(f"⚠️ Database error during authentication: {e}")
            return None

        finally:
            #conn.close() #<- close individal user database connection
            self.connection_pool.putconn(conn)  # ← Returns connectio to pool

    # Takes dependency injection and inserts data into postgres
    def create_user(self, username, password, email=None):
        # 1. Hash Password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # 2. Connect to database
        conn = None
        try:
            # conn = psycopg2.connect(self.database_url) #<- Intividual connetion by user 
            conn = self.connection_pool.getconn() #Use connection pooling
            # 3. INSERT query
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
                    (username, hashed, email)
                )
                conn.commit()
                return True  # Lyckades!
            # 4. Error managemend (username aleady exists?)
            except psycopg2.IntegrityError as e:
                logger.error(f"⚠️ Data already exists - conflict?: {e}")
                return False  # Username finns redan (PRIMARY KEY konflikt)
        
        except Exception as e:
            logger.error(f" ❌ Failed to get database connection: {e}")
            return None  # Retur None = "login failed"
        
        #Stäng anslutningen till DB oavsett fel,
        finally:
            if conn is not None:  # ← Kolla att conn finns
                #conn.close() #<- close individal user database connection
                self.connection_pool.putconn(conn)  # ← Returns connectio to pool

    #Verify login, compare password hashes
    def authenticate(self, username, password):
        # 2. Connect to database
        # conn = psycopg2.connect(self.database_url) #<- Intividual connetion by user 
        conn = self.connection_pool.getconn() #Use connection pooling
    
        try:
            # 2. Hämta password_hash från databas
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password_hash FROM users WHERE username = %s",
                (username,)
            )
            result = cursor.fetchone()
        
            # 3. Om användaren inte finns
            if result is None:
                return None
        
            password_hash = result[0]  # fetchone() returnerar tuple: (password_hash,)

            # Konvertera memoryview till bytes
            if isinstance(password_hash, memoryview):
                password_hash = bytes(password_hash)
        
            # 4. Verifiera lösenord
            if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                # 5. Rätt lösenord → skapa User-objekt
                from auth.models import User
                logger.debug("✅Password hash verified, use object created")
                return User(username)
            else:
                # 6. Fel lösenord
                return None
            
        finally:
            # 7. Close/return database connection
            #conn.close() #<- close individal user database connection
            self.connection_pool.putconn(conn)  # ← Returns connectio to pool

    def get_user(self, username):
        # 1. Connect to database
        conn = None
        try:
            # conn = psycopg2.connect(self.database_url) #<- Intividual connetion by user 
            conn = self.connection_pool.getconn() #Use connection pooling

            # 3. Get user data and create user object
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT username, email, created_at FROM users WHERE username = %s",
                    (username,)
                )
                result = cursor.fetchone()
                
                if result is None:
                    return None
                
                # result är tuple: (username, email, created_at)
                from auth.models import User
                return User(
                    username=result[0],
                    email=result[1],
                    created_at=result[2]
                )
            except Exception as e:
                logger.error(f"Database error fetching user '{username}': {e}")
                return None
    
        except Exception as e:
            logger.error(f"Failed to get database connection: {e}")
            return None

        finally:
            # 3. Close/return database connection if it exists
            if conn is not None:  # ← Kolla att conn finns
                #conn.close() #<- close individal user database connection
                self.connection_pool.putconn(conn)  # ← Returns connectio to pool   

    # Updates a user's password after verifying their old one
    def change_password(self, username, old_password, new_password):
        # Get a connection from the pool
        conn = self.connection_pool.getconn()
        try:
            cursor = conn.cursor()

            # Fetch the current stored password hash for this user
            cursor.execute(
                "SELECT password_hash FROM users WHERE username = %s",
                (username,)
            )
            result = cursor.fetchone()

            # User not found in database
            if result is None:
                return False

            password_hash = result[0]

            # psycopg2 returns BYTEA columns as memoryview — convert to bytes
            if isinstance(password_hash, memoryview):
                password_hash = bytes(password_hash)

            # Verify the supplied old password matches the stored hash
            if not bcrypt.checkpw(old_password.encode('utf-8'), password_hash):
                return False  # Old password is wrong — reject the update

            # Hash the new password with a fresh random salt
            new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            # Persist the new password hash to the users table
            cursor.execute(
                "UPDATE users SET password_hash = %s WHERE username = %s",
                (new_hash, username)
            )
            conn.commit()
            logger.debug(f"✅ Password updated successfully for user '{username}'")
            return True

        except Exception as e:
            # Roll back any partial changes if something went wrong
            conn.rollback()
            logger.error(f"❌ change_password error for '{username}': {e}")
            raise

        finally:
            # Always close cursor and return connection to the pool
            cursor.close()
            self.connection_pool.putconn(conn)

    #Create admin user when auth manager initialises (see __Init__)
    def create_default_admin(self):
        import os

        #Loads variable from .env
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    

        if self.get_user('admin'):
            return  # Admin finns redan
    
        self.create_user('admin', admin_password, 'admin@salesgroup.se')
        print("✅ Admin-användare skapad")
     


