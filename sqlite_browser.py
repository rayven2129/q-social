#!/usr/bin/env python3
"""
Simple SQLite database browser for the e-commerce platform.
This script provides a command-line interface to browse and query the database.
"""

import sqlite3
import os
import sys
from tabulate import tabulate
from app import app

def get_database_path():
    """Get the path to the SQLite database file."""
    database_url = app.config['SQLALCHEMY_DATABASE_URI']
    if database_url.startswith('sqlite:///'):
        db_path = database_url.replace('sqlite:///', '')
        # Check if it's a relative path and if the file exists in instance folder
        if not os.path.isabs(db_path) and not os.path.exists(db_path):
            instance_path = os.path.join('instance', db_path)
            if os.path.exists(instance_path):
                return instance_path
        return db_path
    return 'ecommerce.db'

def connect_to_database():
    """Connect to the SQLite database."""
    db_path = get_database_path()
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        print("Run 'python setup_database.py' to create the database first.")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def list_tables():
    """List all tables in the database."""
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print("📋 Database Tables:")
        print("-" * 20)
        for table in tables:
            try:
                # Use quotes around table name to handle reserved keywords
                cursor.execute(f'SELECT COUNT(*) FROM "{table["name"]}"')
                count = cursor.fetchone()[0]
                print(f"  {table['name']} ({count} records)")
            except Exception as e:
                print(f"  {table['name']} (error: {e})")
        
    except Exception as e:
        print(f"❌ Error listing tables: {e}")
    finally:
        conn.close()

def show_table_schema(table_name):
    """Show the schema for a specific table."""
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        if not columns:
            print(f"❌ Table '{table_name}' not found")
            return
        
        print(f"📊 Schema for table '{table_name}':")
        print("-" * 40)
        
        headers = ['Column', 'Type', 'Not Null', 'Default', 'Primary Key']
        rows = []
        for col in columns:
            rows.append([
                col['name'],
                col['type'],
                'Yes' if col['notnull'] else 'No',
                col['dflt_value'] or '',
                'Yes' if col['pk'] else 'No'
            ])
        
        print(tabulate(rows, headers=headers, tablefmt='grid'))
        
    except Exception as e:
        print(f"❌ Error showing schema: {e}")
    finally:
        conn.close()

def browse_table(table_name, limit=10):
    """Browse records in a specific table."""
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        # Use quotes around table name to handle reserved keywords
        cursor.execute(f'SELECT * FROM "{table_name}" LIMIT {limit}')
        records = cursor.fetchall()
        
        if not records:
            print(f"📭 No records found in table '{table_name}'")
            return
        
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        print(f"📋 Records from table '{table_name}' (showing first {limit}):")
        print("-" * 60)
        
        # Convert records to list of lists for tabulate
        rows = []
        for record in records:
            rows.append(list(record))
        
        print(tabulate(rows, headers=column_names, tablefmt='grid'))
        
        # Show total count
        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        total = cursor.fetchone()[0]
        print(f"\nTotal records in {table_name}: {total}")
        
    except Exception as e:
        print(f"❌ Error browsing table: {e}")
    finally:
        conn.close()

def execute_query(query):
    """Execute a custom SQL query."""
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            records = cursor.fetchall()
            if records:
                column_names = [description[0] for description in cursor.description]
                rows = [list(record) for record in records]
                print(tabulate(rows, headers=column_names, tablefmt='grid'))
                print(f"\nRows returned: {len(records)}")
            else:
                print("📭 No results found")
        else:
            conn.commit()
            print(f"✅ Query executed successfully. Rows affected: {cursor.rowcount}")
        
    except Exception as e:
        print(f"❌ Error executing query: {e}")
    finally:
        conn.close()

def show_database_info():
    """Show general database information."""
    conn = connect_to_database()
    if not conn:
        return
    
    try:
        db_path = get_database_path()
        file_size = os.path.getsize(db_path)
        
        # Convert file size to human readable format
        for unit in ['B', 'KB', 'MB', 'GB']:
            if file_size < 1024.0:
                size_str = f"{file_size:.1f} {unit}"
                break
            file_size /= 1024.0
        
        print("📊 Database Information:")
        print("-" * 30)
        print(f"File: {os.path.abspath(db_path)}")
        print(f"Size: {size_str}")
        
        # Get SQLite version
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version()")
        sqlite_version = cursor.fetchone()[0]
        print(f"SQLite Version: {sqlite_version}")
        
        # Get table count
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]
        print(f"Tables: {table_count}")
        
    except Exception as e:
        print(f"❌ Error getting database info: {e}")
    finally:
        conn.close()

def interactive_mode():
    """Start interactive mode for database browsing."""
    print("🔍 SQLite Database Browser - Interactive Mode")
    print("Type 'help' for available commands or 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            command = input("\nsqlite> ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif command.lower() == 'help':
                print_help()
            elif command.lower() == 'tables':
                list_tables()
            elif command.lower() == 'info':
                show_database_info()
            elif command.lower().startswith('schema '):
                table_name = command.split(' ', 1)[1]
                show_table_schema(table_name)
            elif command.lower().startswith('browse '):
                parts = command.split(' ')
                table_name = parts[1]
                limit = int(parts[2]) if len(parts) > 2 else 10
                browse_table(table_name, limit)
            elif command.strip():
                execute_query(command)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def print_help():
    """Print help information."""
    print("\n📖 Available Commands:")
    print("-" * 30)
    print("  tables              - List all tables")
    print("  info                - Show database information")
    print("  schema <table>      - Show table schema")
    print("  browse <table> [n]  - Browse table records (limit n, default 10)")
    print("  SELECT ...          - Execute custom SQL query")
    print("  help                - Show this help")
    print("  quit/exit/q         - Exit the browser")

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) == 1:
        interactive_mode()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'tables':
        list_tables()
    elif command == 'info':
        show_database_info()
    elif command == 'schema' and len(sys.argv) > 2:
        show_table_schema(sys.argv[2])
    elif command == 'browse' and len(sys.argv) > 2:
        table_name = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        browse_table(table_name, limit)
    elif command == 'query' and len(sys.argv) > 2:
        query = ' '.join(sys.argv[2:])
        execute_query(query)
    else:
        print("Usage: python sqlite_browser.py [command] [args]")
        print("Commands:")
        print("  tables                    - List all tables")
        print("  info                      - Show database information")
        print("  schema <table>            - Show table schema")
        print("  browse <table> [limit]    - Browse table records")
        print("  query '<SQL>'             - Execute custom SQL query")
        print("  (no args)                 - Start interactive mode")

if __name__ == '__main__':
    # Check if tabulate is available
    try:
        from tabulate import tabulate as tab_func
        # Test tabulate function
        test_result = tab_func([['test']], headers=['Test'])
    except ImportError:
        print("❌ 'tabulate' package is required for table formatting")
        print("Install it with: pip install tabulate")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error with tabulate: {e}")
        sys.exit(1)
    
    main()
