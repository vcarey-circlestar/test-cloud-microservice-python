from flask import Flask, jsonify, request
import psycopg2
import os, json

app = Flask(__name__)

# --- Database Configuration ---
#  Ideally, these should come from environment variables for security
#  and portability.
DB_HOST = os.environ.get("DB_HOST", "your_db_host")  # e.g., 127.0.0.1 or cloud sql instance connection name
DB_NAME = os.environ.get("DB_NAME", "your_db_name")
DB_USER = os.environ.get("DB_USER", "your_db_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "your_db_password")
DB_PORT = os.environ.get("DB_PORT", 5432)  # Default PostgreSQL port

# --- Error Handling ---
class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass


def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            sslmode="verify-ca"
            sslcert='/mnt1/cr-sql-client-cert'
            sslkey='/mnt2/cr-sql-client-key'
            sslrootcert='/mnt3/cr-sql-server-ca'
        )
        return conn
    except psycopg2.Error as e:
        raise DatabaseError(f"Error connecting to the database: {e}")


def close_db_connection(conn):
    """Closes the database connection."""
    if conn:
        conn.close()


def get_table_names(conn, schema="public"):
    """
    Retrieves a list of table names from the specified schema.

    Args:
        conn: The database connection object.
        schema: The schema to query (default: 'public').

    Returns:
        A list of table names.
    """
    try:
        cursor = conn.cursor()
        # Query to get table names in the specified schema
        query = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s
            AND table_type = 'BASE TABLE';
        """
        cursor.execute(query, (schema,))
        table_names = [row[0] for row in cursor.fetchall()]
        return table_names
    except psycopg2.Error as e:
        raise DatabaseError(f"Error querying table names: {e}")
    finally:
        cursor.close()


@app.route('/api/tables', methods=['GET'])
def list_tables():
    """API endpoint to list table names."""
    schema = request.args.get("schema", "public")
    conn = None  # Initialize to None for proper error handling

    try:
        conn = get_db_connection()
        tables = get_table_names(conn, schema)
        return jsonify({"tables": tables})
    except DatabaseError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500
    finally:
        close_db_connection(conn)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=DB_PORT)
