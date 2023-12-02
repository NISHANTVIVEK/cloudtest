from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Replace these values with your Redshift cluster information
dbname = 'dev'
user = 'admin'
password = 'Admin12345'
host = 'diabetes-workgroup.604998347852.eu-west-1.redshift-serverless.amazonaws.com'
port = '5439'

def get_redshift_data():
    try:
        # Establish a connection to the Redshift cluster
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Example: Execute a query
        cursor.execute("SELECT * from dev.public.diabetes WHERE smoking_history ='never' and age > 50")
        rows = cursor.fetchall()

        # Convert the results to a list of dictionaries
        data = [{'column1': row[0], 'column2': row[1]} for row in rows]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return data

    except Exception as e:
        print("Error: Unable to connect to the database.")
        print(e)
        return []

@app.route('/get_data', methods=['GET'])
def get_data():
    data = get_redshift_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
