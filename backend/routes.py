from flask import jsonify, request

from database import get_connection


def register_routes(app):

    # ---------------------------------
    # GET TODOS + SEARCH + FILTER
    # ---------------------------------

    @app.route("/todos", methods=["GET"])
    def get_todos():

        conn = None
        cursor = None

        try:
            conn = get_connection()
            cursor = conn.cursor()

            search = request.args.get("search")
            completed = request.args.get("completed")

            conditions = []
            values = []

            # Search filter
            if search:
                conditions.append("task ILIKE %s")
                values.append(f"%{search}%")

            # Completed / Pending filter
            if completed is not None:

                if completed == "true":
                    completed_value = True

                elif completed == "false":
                    completed_value = False

                else:
                    return jsonify({
                        "error": "completed must be true or false"
                    }), 400

                conditions.append("completed = %s")
                values.append(completed_value)

            # Build query
            query = "SELECT * FROM todos"

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            cursor.execute(query, tuple(values))

            rows = cursor.fetchall()

            todos = []

            for row in rows:

                todo = {
                    "id": row[0],
                    "task": row[1],
                    "completed": row[2]
                }

                todos.append(todo)

            return jsonify(todos), 200

        except Exception as e:

            print("❌ Error fetching todos:", e)

            return jsonify({
                "error": "Unable to fetch todos"
            }), 500

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()


    # ---------------------------------
    # ADD TODO
    # ---------------------------------

    @app.route("/todos", methods=["POST"])
    def add_todo():

        conn = None
        cursor = None

        try:

            data = request.get_json()

            # Input validation
            if not data:
                return jsonify({
                    "error": "Request body is required"
                }), 400

            task = data.get("task")

            if not task:
                return jsonify({
                    "error": "Task is required"
                }), 400

            task = task.strip()

            if not task:
                return jsonify({
                    "error": "Task cannot be empty"
                }), 400

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO todos(task, completed)
                VALUES(%s, %s)
                """,
                (task, False)
            )

            conn.commit()

            return jsonify({
                "message": "Todo added successfully"
            }), 201

        except Exception as e:

            print("❌ Error adding todo:", e)

            if conn:
                conn.rollback()

            return jsonify({
                "error": "Unable to add todo"
            }), 500

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()


    # ---------------------------------
    # UPDATE TODO
    # ---------------------------------

    @app.route("/todos/<int:todo_id>", methods=["PUT"])
    def update_todo(todo_id):

        conn = None
        cursor = None

        try:

            data = request.get_json()

            if not data:
                return jsonify({
                    "error": "Request body is required"
                }), 400

            task = data.get("task")
            completed = data.get("completed")

            # Validate task
            if not task:
                return jsonify({
                    "error": "Task is required"
                }), 400

            task = task.strip()

            if not task:
                return jsonify({
                    "error": "Task cannot be empty"
                }), 400

            # Validate completed
            if not isinstance(completed, bool):
                return jsonify({
                    "error": "completed must be true or false"
                }), 400

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE todos
                SET task = %s,
                    completed = %s
                WHERE id = %s
                """,
                (task, completed, todo_id)
            )

            # Check whether todo exists
            if cursor.rowcount == 0:
                return jsonify({
                    "error": "Todo not found"
                }), 404

            conn.commit()

            return jsonify({
                "message": "Task updated successfully"
            }), 200

        except Exception as e:

            print("❌ Error updating todo:", e)

            if conn:
                conn.rollback()

            return jsonify({
                "error": "Unable to update todo"
            }), 500

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()


    # ---------------------------------
    # DELETE TODO
    # ---------------------------------

    @app.route("/todos/<int:todo_id>", methods=["DELETE"])
    def delete_todo(todo_id):

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM todos
                WHERE id = %s
                """,
                (todo_id,)
            )

            if cursor.rowcount == 0:
                return jsonify({
                    "error": "Todo not found"
                }), 404

            conn.commit()

            return jsonify({
                "message": "Task deleted successfully"
            }), 200

        except Exception as e:

            print("❌ Error deleting todo:", e)

            if conn:
                conn.rollback()

            return jsonify({
                "error": "Unable to delete todo"
            }), 500

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()


    # ---------------------------------
    # STATISTICS
    # ---------------------------------

    @app.route("/todos/stats", methods=["GET"])
    def get_statistics():

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(*) AS total,
                    COUNT(*) FILTER (WHERE completed = TRUE) AS completed,
                    COUNT(*) FILTER (WHERE completed = FALSE) AS pending
                FROM todos
                """
            )

            row = cursor.fetchone()

            stats = {
                "total": row[0],
                "completed": row[1],
                "pending": row[2]
            }

            return jsonify(stats), 200

        except Exception as e:

            print("❌ Error getting statistics:", e)

            return jsonify({
                "error": "Unable to get statistics"
            }), 500

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()