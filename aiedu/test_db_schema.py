from database.database_schema import InitializeDatabase

def main():
    db_initializer = InitializeDatabase()
    db_initializer.initialize_schema()

if __name__ == "__main__":
    main()