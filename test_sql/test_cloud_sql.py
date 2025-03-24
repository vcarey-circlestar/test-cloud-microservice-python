from flask import Flask, jsonify, request
import psycopg2
import os, json, io, tempfile
from google.cloud import secretmanager

app = Flask(__name__)

# --- Enviromnent Vars for Database Access ---
#  Environment variables configured in cloud run (some from secrets)
DB_HOST = os.environ.get("DB_HOST", "your_db_host") 
DB_NAME = os.environ.get("DB_NAME", "your_db_name")
DB_USER = os.environ.get("DB_USER", "your_db_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "your_db_password")
DB_PORT = os.environ.get("DB_PORT", 5432)  # Default PostgreSQL port
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "circlestar-2024")

# --- Secret retrieval ---
# For SSL files
def access_secret_version(secret_id, project_id = PROJECT_ID):
    """Access the payload for the given secret version if one exists."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest" 
    response = client.access_secret_version(name=name)
    content = response.payload.data.decode('UTF-8')
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.pem') as tmp_file:
        tmp_file.write(content)
        tmp_file.flush()
    return tmp_file.name

client_cert = access_secret_version('cr-sql-client-cert') 
client_key = access_secret_version('cr-sql-client-key')
server_ca = access_secret_version('cr-sql-server-ca')


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
            sslmode="require",
            sslcert=client_cert,
            sslkey=client_key,
            sslrootcert=server_ca
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
