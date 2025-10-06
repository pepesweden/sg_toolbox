import psycopg2 
import bcrypt

class AuthManager:
    # saves database URL to variable
    def __init__(self, database_url):
        self.database_url = database_url
        self.create_default_admin()

    # Takes dependency injection and inserts data into postgres
    def create_user(self, username, password, email=None):
        # 1. Hasha lösenord
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # 2. Connecta till databas
        conn = psycopg2.connect(self.database_url)
        # 3. INSERT query
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
                (username, hashed, email)
            )
            conn.commit()
            return True  # Lyckades!
        # 4. Hantera fel (username finns redan?)
        except psycopg2.IntegrityError:
            return False  # Username finns redan (PRIMARY KEY konflikt)
        #Stäng anslutningen till DB oavsett fel,
        finally:
            conn.close() 

    #Verify login, compare password hashes
    def authenticate(self, username, password):
        # 1. Connecta till databas
        conn = psycopg2.connect(self.database_url)
    
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
        
            # 4. Verifiera lösenord
            if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                # 5. Rätt lösenord → skapa User-objekt
                from auth.models import User
                return User(username)
            else:
                # 6. Fel lösenord
                return None
            
        finally:
            # 7. Stäng connection
            conn.close()

    def get_user(self, username):
        conn = psycopg2.connect(self.database_url)
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
        finally:
            conn.close()   

    #Create admin user when auth manager initialises (see __Init__)    
    def create_default_admin(self):
        import os

        #Loads variable from .env
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    

        if self.get_user('admin'):
            return  # Admin finns redan
    
        self.create_user('admin', admin_password, 'admin@salesgroup.se')
        print("✅ Admin-användare skapad")
     


