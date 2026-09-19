from flask import Flask, jsonify, request
app = Flask(__name__)

import psycopg2
@app.route("/todos", methods = ["GET"])
def get_todos():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
        host="localhost",
        database="todo_db",
        user="postgres",
        password="postgres@123",
        port="5432"
    )
        print("✅ Connected Successfully!")

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos")
        rows = cursor.fetchall()
        todos = []
        for row in rows:
            todo = {
            "id": row[0],
            "task": row[1],
            "completed": row[2]
        }
            todos.append(todo)
        return jsonify(todos)
    except Exception as e:
        print("❌ Connection Failed")
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@app.route("/todos", methods = ["POST"])
def add_todos():
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
        host="localhost",
        database="todo_db",
        user="postgres",
        password="postgres@123",
        port="5432"
    )
        print("✅ Connected Successfully!")
        data = request.get_json()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO TODOS(task, completed) VALUES(%s,%s)",
                   (data["task"], False))
        
        conn.commit()
        return jsonify({"message": "Todo added successfully"})
    except Exception as e:
        print("❌ Connection Failed")
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()      

@app.route("/todos/<int:todo_id>", methods = ["PUT"])
def update_todo(todo_id):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
        host="localhost",
        database="todo_db",
        user="postgres",
        password="postgres@123",
        port="5432"
        )
        print("✅ Connected Successfully!")
        data = request.get_json()
        task = data["task"]
        completed = data["completed"]
        cursor = conn.cursor()
        cursor.execute("""UPDATE todos
                          SET task = %s,
                          completed = %s
                          WHERE ID = %s
                        """,
                        (task, completed, todo_id)
        )        
        conn.commit()
        return jsonify({"message": "Task updated successfully"})
    except Exception as e:
            print("❌ Connection Failed")
            print(e)
    finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()   

@app.route("/todos/<int:todo_id>", methods = ["DELETE"])
def delete_todo(todo_id):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
        host="localhost",
        database="todo_db",
        user="postgres",
        password="postgres@123",
        port="5432"
        )
        print("✅ Connected Successfully!")
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM todos
                          WHERE id = %s
                        """,
                            (todo_id,)
        )        
        conn.commit()
        return jsonify({"message": "Task deleted successfully"})
    except Exception as e:
            print("❌ Connection Failed")
            print(e)
    finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

if __name__ == "__main__":
    app.run(debug=True)
