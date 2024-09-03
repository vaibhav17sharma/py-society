from mysql.connector import Error;

def create_tables(connection):
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS towers (
            tower_id INT AUTO_INCREMENT PRIMARY KEY,
            tower_name VARCHAR(50) NOT NULL,
            address VARCHAR(255)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS flats (
            flat_id INT AUTO_INCREMENT PRIMARY KEY,
            flat_number VARCHAR(10) NOT NULL,
            tower_id INT,
            floor_number INT,
            flat_type VARCHAR(50),
            FOREIGN KEY (tower_id) REFERENCES towers(tower_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS residents (
            resident_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            date_of_birth DATE,
            phone_number VARCHAR(15),
            email VARCHAR(100),
            flat_id INT,
            FOREIGN KEY (flat_id) REFERENCES flats(flat_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS parkings (
            parking_id INT AUTO_INCREMENT PRIMARY KEY,
            flat_id INT,
            parking_spot_number VARCHAR(10) NOT NULL,
            allocation_date DATE,
            FOREIGN KEY (flat_id) REFERENCES flats(flat_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS combined_charges (
            charge_id INT AUTO_INCREMENT PRIMARY KEY,
            flat_id INT,
            charge_month DATE,
            charge_type ENUM('Electricity', 'Maintenance'),
            amount DECIMAL(10, 2),
            payment_status VARCHAR(20),
            due_date DATE,
            payment_date DATE,
            FOREIGN KEY (flat_id) REFERENCES flats(flat_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('Admin', 'Staff', 'Resident'),
            email VARCHAR(100)
        )
        """)

        # Commit changes
        connection.commit()
        print("Tables created successfully.")
        seed_data(connection)

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def check_table_empty(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        return count == 0
    except Error as e:
        print(f"Error checking table '{table_name}': {e}")
        return False
    finally:
        cursor.close()

def seed_data(connection):
    try:
        cursor = connection.cursor()

        # Seed data for `towers` table
        if check_table_empty(connection, 'towers'):
            towers = [
                ('Tower A', '1234 Elm Street'),
                ('Tower B', '5678 Oak Avenue')
            ]
            cursor.executemany("""
                INSERT INTO towers (tower_name, address)
                VALUES (%s, %s)
            """, towers)
            print("Data seeded into 'towers' table.")

        # Seed data for `flats` table
        if check_table_empty(connection, 'flats'):
            flats = [
                ('101', 1, 1, '2BHK'),
                ('202', 1, 2, '3BHK'),
                ('303', 2, 3, '1BHK')
            ]
            cursor.executemany("""
                INSERT INTO flats (flat_number, tower_id, floor_number, flat_type)
                VALUES (%s, %s, %s, %s)
            """, flats)
            print("Data seeded into 'flats' table.")

        # Seed data for `residents` table
        if check_table_empty(connection, 'residents'):
            residents = [
                ('John', 'Doe', '1980-01-01', '123-456-7890', 'john.doe@example.com', 1),
                ('Jane', 'Smith', '1990-02-02', '987-654-3210', 'jane.smith@example.com', 2)
            ]
            cursor.executemany("""
                INSERT INTO residents (first_name, last_name, date_of_birth, phone_number, email, flat_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, residents)
            print("Data seeded into 'residents' table.")

        # Seed data for `parkings` table
        if check_table_empty(connection, 'parkings'):
            parkings = [
                (1, 'A1', '2024-01-01'),
                (2, 'B2', '2024-01-15')
            ]
            cursor.executemany("""
                INSERT INTO parkings (flat_id, parking_spot_number, allocation_date)
                VALUES (%s, %s, %s)
            """, parkings)
            print("Data seeded into 'parkings' table.")

        # Seed data for `combined_charges` table
        if check_table_empty(connection, 'combined_charges'):
            charges = [
                (1, '2024-09-01', 'Electricity', 100.00, 'Paid', '2024-09-10', '2024-09-05'),
                (2, '2024-09-01', 'Maintenance', 50.00, 'Unpaid', '2024-09-30', None)
            ]
            cursor.executemany("""
                INSERT INTO combined_charges (flat_id, charge_month, charge_type, amount, payment_status, due_date, payment_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, charges)
            print("Data seeded into 'combined_charges' table.")

        # Seed data for `users` table
        if check_table_empty(connection, 'users'):
            users = [
                ('admin', 'hashed_password_1', 'Admin', 'admin@example.com'),
                ('staff1', 'hashed_password_2', 'Staff', 'staff1@example.com'),
                ('resident1', 'hashed_password_3', 'Resident', 'resident1@example.com')
            ]
            cursor.executemany("""
                INSERT INTO users (username, password_hash, role, email)
                VALUES (%s, %s, %s, %s)
            """, users)
            print("Data seeded into 'users' table.")

        # Commit changes
        connection.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def get_residents(connection, flat_id=None, tower_id=None):
    try:
        cursor = connection.cursor()
        
        if flat_id is not None:
            query = "SELECT f.flat_number,r.first_name, r.last_name, r.date_of_birth, r.phone_number, f.flat_type  FROM residents r LEFT JOIN flats f ON r.flat_id = f.flat_id WHERE r.flat_id = %s"
            params = (flat_id,)
        elif tower_id is not None:
            query = "SELECT f.flat_number,r.first_name, r.last_name, r.date_of_birth, r.phone_number, f.flat_type  FROM residents r LEFT JOIN flats f ON r.flat_id = f.flat_id WHERE f.tower_id = %s"
            params = (tower_id,)
        else:
            query = "SELECT f.flat_number,r.first_name, r.last_name, r.date_of_birth, r.phone_number, f.flat_type  FROM residents r LEFT JOIN flats f ON r.flat_id = f.flat_id"
            params = ()
        
        cursor.execute(query, params)
        residents = cursor.fetchall()
        return residents
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()

def get_flats(connection,tower_id=None):
    try:
        cursor = connection.cursor()
        if tower_id is None:
            cursor.execute("SELECT * FROM flats")
        else:
            query = "SELECT * FROM flats WHERE tower_id = %s"
            cursor.execute(query, (tower_id,))

        flats = cursor.fetchall()
        return flats
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()

def get_parkings(connection, allotted=None):
    try:
        cursor = connection.cursor()
        if allotted is not None:
            if allotted:
                query = "SELECT * FROM parkings WHERE flat_id IS NOT NULL"
            else:
                query = "SELECT * FROM parkings WHERE flat_id IS NULL"
            params = ()
        else:
            query = "SELECT * FROM parkings"
            params = ()
        cursor.execute(query, params)
        parkings = cursor.fetchall()
        return parkings
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()

def get_combined_charges(connection,flat_id=None):
    try:
        cursor = connection.cursor()
        if flat_id is not None:
            query = """
                SELECT SUM(amount) as total_charges
                FROM combined_charges
                WHERE flat_id = %s AND payment_status = 'Unpaid'
            """
            params = (flat_id,)
        else:
            query = """
                SELECT flat_id
                FROM combined_charges
                WHERE payment_status = 'Unpaid'
                GROUP BY flat_id
            """
            params = ()
        
        cursor.execute(query, params)
        result = cursor.fetchall()
        
        if flat_id is not None:
            if result:
                return result[0][0] 
            return 0 
        else:
            return [row[0] for row in result]
    
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()

def add_resident(connection, flat_id, first_name, last_name, date_of_birth, phone_number, email):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO residents (flat_id, first_name, last_name, date_of_birth, phone_number, email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (flat_id, first_name, last_name, date_of_birth, phone_number, email)
        cursor.execute(query, params)
        connection.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()

def add_parking(connection, flat_id, parking_spot_number, allocation_date):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO parkings (flat_id, parking_spot_number, allocation_date)
            VALUES (%s, %s, %s)
        """
        params = (flat_id, parking_spot_number, allocation_date)
        cursor.execute(query, params)
        connection.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()

def add_combined_charge(connection, flat_id, charge_month, charge_type, amount, payment_status, due_date, payment_date):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO combined_charges (flat_id, charge_month, charge_type, amount, payment_status, due_date, payment_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (flat_id, charge_month, charge_type, amount, payment_status, due_date, payment_date)
        cursor.execute(query, params)
        connection.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
    
def add_flat(connection, flat_number, tower_id, floor_number, flat_type):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO flats (flat_number, tower_id, floor_number, flat_type)
            VALUES (%s, %s, %s, %s)
        """
        params = (flat_number, tower_id, floor_number, flat_type)
        cursor.execute(query, params)
        connection.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
    
def add_tower(connection, tower_name, address):
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO towers (tower_name, address)
            VALUES (%s, %s)
        """
        params = (tower_name, address)
        cursor.execute(query, params)
        connection.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()