import psycopg2
from psycopg2 import Binary
from psycopg2 import sql
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify

def connect_db():
    db_config = { "host":"dpg-cjtf2a15mpss73d3rv1g-a.oregon-postgres.render.com",
    "user":"chat_sql_db_user",
    "dbname":"chat_sql_db",
    "password":"i5QNFqt3VJy0y5PQEBsRc35GvbejWymi",
    "port" : "5432"}

    connection = psycopg2.connect(**db_config)
    return connection   
    

def createuser(uniqueid,name,role,userId,upload=False):
    connection = connect_db()
    cursor = connection.cursor()

    exist_query = """SELECT uuid from userData
                        WHERE user_id=%s AND name=%s AND role=%s"""

    cursor.execute(exist_query, (userId, name, role))
    result = cursor.fetchone()

    if result:
        return {"exist": True ,"uuid": result[0]}

    create_query = """INSERT INTO userData (uuid,name,role,upload, user_id)
                        VALUES (%s,%s,%s,%s,%s)
                   """
    
    cursor.execute(create_query,(uniqueid,name,role,upload,userId))
    connection.commit()
    
    if connection:
        connection.close()

    if cursor:
        cursor.close()

    return {"exist": False}
    
def setopenai(uniqueid,openkey):
    connection = connect_db()
    cursor = connection.cursor()

    query_op = """UPDATE userData
                SET openai=%s where uuid=%s
                """
    
    cursor.execute(query_op,(openkey,uniqueid))
    connection.commit()

    if connection:
        connection.close()

    if cursor:
        cursor.close()

    return True


def openkey(uniqueid):
    connection = connect_db()
    cursor = connection.cursor()

    open_query = """SELECT openai FROM userData
                    WHERE uuid=%s
                    """
    
    cursor.execute(open_query,(uniqueid,))
    result = cursor.fetchone()
    if connection:
        connection.close()

    if cursor:
        cursor.close()

    return result[0]


def set_file(uniqueid,filedata,filename,upload=True):
    connection = connect_db()
    cursor = connection.cursor()

    query = """UPDATE userData SET
            upload = %s, filename = %s, filedata =%s
            WHERE uuid = %s;
            """
    filedata = Binary(filedata).getquoted()
    cursor.execute(query,(upload,filename,filedata,uniqueid))
    connection.commit()

    if connection:
        connection.close()
        cursor.close()

    return True


def get_file(uniqueid):
    connection = connect_db()
    cursor = connection.cursor()

    query = """SELECT filedata FROM userData
                Where uuid = %s
            """
    
    cursor.execute(query,(uniqueid,))
    result = cursor.fetchone()

    connection.close()
    cursor.close()

    return result[0]

def loginUser(email, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user[3], password):
        return jsonify({'message': 'Login successful', 'user_id': user[0]}), 200
    else:
        return jsonify({'error': 'Login failed. Please check your email and password'}), 401

def registerUser(name, email, password):
    hashed_password = generate_password_hash(password, method='sha256')

    try:
        conn = connect_db()
        cursor = conn.cursor()

        insert_query = sql.SQL("""
            INSERT INTO users (name, email, password)
            VALUES ({}, {}, {})
            RETURNING id
        """).format(sql.Literal(name), sql.Literal(email), sql.Literal(hashed_password))

        cursor.execute(insert_query)
        user_id = cursor.fetchone()[0]
        conn.commit()

        return jsonify({'message': 'Registration successful', 'user_id': user_id}), 201

    except psycopg2.IntegrityError as e:
        conn.rollback()
        return jsonify({'error': 'Email already registered'}), 400
    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'An error occurred'}), 500
    finally:
        conn.close()
    
def main():
    print("inside main!")


if __name__ == "__main__":
    main()
