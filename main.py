import db_connector
import time
import queries

def loading_screen():
    print("\nSetting up the Society Management System",end="")
    for i in range(5):
        print(".", end="", flush=True)
        time.sleep(0.2)
    print("\n") 

def clear_console():
    print("\033[H\033[J", end='')

def print_table(headers, data):
    column_widths = [max(len(header), max(len(str(row[i])) for row in data)) for i, header in enumerate(headers)]
    header_row = " | ".join(header.ljust(width) for header, width in zip(headers, column_widths))
    print(header_row)
    print("-" * len(header_row))  # Separator line
    for row in data:
        print(" | ".join(str(cell).ljust(width) for cell, width in zip(row, column_widths)))

def intro(connection):
    print("\n" + "="*50)
    print(" Welcome to the Society Management System")
    print("="*50)
    print("\n\nInitializing the system...")
    
    loading_screen()
    db_connector.create_database(connection,"society")
    queries.create_tables(connection) 

    print("\nSystem setup complete!")
    print("\nYou are now ready to manage your society.\n")

    input("Press Enter to move to the next step...")
    clear_console()
    
def display_menu():
    print("\n" + "="*50)
    print("        Society Management System Menu")
    print("="*50)
    print("1. Add New Resident")
    print("2. Add New Flat")
    print("3. Add New Tower")
    print("4. Add New Parking")
    print("5. Add New Charges")
    print("6. Get Residents information by flat ID")
    print("7. Get Residents list by Tower ID")
    print("8. Allot Parking")
    print("9. Get unpaid charges")
    print("10. Get Unallotted Parking")
    print("11. Exit")
    print("="*30)
    
    choice = input("Please select an option (1-4): ")
    return choice

def process_choice(choice,connection):
    clear_console()

    if choice == "1":
        print("You selected Sample Option 1.")
        addResident(connection)

    elif choice == "2":
        print("You selected Sample Option 2.")
        addFlat(connection)

    elif choice == "3":
        print("You selected Sample Option 3.")
        addTower(connection)
        
    elif choice == "4":
        print("You selected Sample Option 4.")
        addParking(connection)
        
    elif choice == "5":
        print("You selected Sample Option 5.")
        addCharges(connection)

    elif choice == "6":
        print("You selected Sample Option 6.")
        getResidents(connection,"flat_id")

    elif choice == "7":
        print("You selected Sample Option 7.")
        getResidents(connection,"tower_id")

    elif choice == "8":
        print("You selected Sample Option 8.")
        
    elif choice == "9":
        print("You selected Sample Option 9.")
        
    elif choice == "10":
        print("You selected Sample Option 10.")

    elif choice == "11":
        print("Exiting the program...")
        return False
    else:
        print("Invalid choice. Please select a valid option.")
    return True

def getResidents(connection,type):
    if type == "flat_id":
        print("Enter the flat ID:",end=" ")
        flat_id = input()
        residents = queries.get_residents(connection, flat_id)
    elif type == "tower_id":
        print("Enter the tower ID:",end=" ")
        tower_id = input()
        residents = queries.get_residents(connection,None, tower_id)
    else:
        print("Invalid choice. Please select a valid option.")
        return
    
    print("Residents list:")
    headers = ["Flat Number","First Name", "Last Name", "Date of Birth", "Phone Number", "Flat Type"]
    print_table(headers,residents)

def addResident(connection):
    print("Enter the flat ID:",end=" ")
    flat_id = input()
    print("Enter the first name:",end=" ")
    first_name = input()
    print("Enter the last name:",end=" ")
    last_name = input()
    print("Enter the date of birth (YYYY-MM-DD):",end=" ")
    date_of_birth = input()
    print("Enter the phone number:",end=" ")
    phone_number = input()
    print("Enter the email:",end=" ")
    email = input()
    
    if queries.add_resident(connection, flat_id, first_name, last_name, date_of_birth, phone_number, email):
        print("Resident added successfully.")
    else:
        print("Error adding resident.")

def addFlat(connection):
    print("Enter the flat number:",end=" ")
    flat_number = input()
    print("Enter the tower ID:",end=" ")
    tower_id = input()
    print("Enter the floor number:",end=" ")
    floor_number = input()
    print("Enter the flat type:",end=" ")
    flat_type = input()
    
    if queries.add_flat(connection, flat_number, tower_id, floor_number, flat_type):
        print("Flat added successfully.")
    else:
        print("Error adding flat.")

def addTower(connection):
    print("Enter the tower name:",end=" ")
    tower_name = input()
    print("Enter the address:",end=" ")
    address = input()
    
    if queries.add_tower(connection, tower_name, address):
        print("Tower added successfully.")
    else:
        print("Error adding tower.")

def addParking(connection):
    print("Enter the flat ID:",end=" ")
    flat_id = input()
    print("Enter the parking spot number:",end=" ")
    parking_spot_number = input()
    print("Enter the allocation date:",end=" ")
    allocation_date = input()
    
    if queries.add_parking(connection, flat_id, parking_spot_number, allocation_date):
        print("Parking added successfully.")
    else:
        print("Error adding parking.")

def addCharges(connection):
    print("Enter the flat ID:",end=" ")
    flat_id = input()
    print("Enter the charge month:",end=" ")
    charge_month = input()
    print("Enter the charge type:",end=" ")
    charge_type = input()
    print("Enter the amount:",end=" ")
    amount = input()
    print("Enter the payment status:",end=" ")
    payment_status = input()
    print("Enter the due date:",end=" ")
    due_date = input()
    print("Enter the payment date:",end=" ")
    payment_date = input()
    
    if queries.add_combined_charge(connection, flat_id, charge_month, charge_type, amount, payment_status, due_date, payment_date):
        print("Charges added successfully.")
    else:
        print("Error adding charges.")

def main():
    connection = db_connector.create_connection()
    intro(connection)

    running = True
    while running:
        user_choice = display_menu()
        running = process_choice(user_choice,connection)

    db_connector.close_connection(connection)
    clear_console()


if __name__ == "__main__":
    main()
