import streamlit as st
import requests


API_URL = "http://localhost:5000"


st.set_page_config(
    page_title="Todo App",
    page_icon="✅",
    layout="centered"
)

st.title("✅ My Todo App")


# ---------------------------------
# SEARCH + FILTER
# ---------------------------------

search = st.text_input(
    "🔍 Search todos",
    placeholder="Search for a task..."
)

filter_option = st.selectbox(
    "Filter",
    ["All", "Completed", "Pending"]
)


# ---------------------------------
# BUILD PARAMETERS
# ---------------------------------

params = {}

if search:
    params["search"] = search

if filter_option == "Completed":
    params["completed"] = True

elif filter_option == "Pending":
    params["completed"] = False


# ---------------------------------
# FETCH TODOS
# ---------------------------------

data = []

try:

    response = requests.get(
        f"{API_URL}/todos",
        params=params
    )

    if response.status_code == 200:
        data = response.json()

    else:
        st.error("Unable to fetch todos")

except Exception as e:

    st.error(f"Connection failed: {e}")


# ---------------------------------
# STATISTICS
# ---------------------------------

try:

    response = requests.get(
        f"{API_URL}/todos/stats"
    )

    if response.status_code == 200:

        stats = response.json()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total",
            stats["total"]
        )

        col2.metric(
            "Completed",
            stats["completed"]
        )

        col3.metric(
            "Pending",
            stats["pending"]
        )

except Exception as e:

    st.error(f"Unable to load statistics: {e}")


st.divider()


# ---------------------------------
# ADD TODO
# ---------------------------------

st.subheader("➕ Add Todo")

task = st.text_input(
    "Enter your task"
)

if st.button("Add Task"):

    if not task.strip():

        st.warning("Please enter a task.")

    else:

        try:

            response = requests.post(
                f"{API_URL}/todos",
                json={
                    "task": task
                }
            )

            if response.status_code in [200, 201]:

                st.success(
                    "Todo added successfully!"
                )

                st.rerun()

            else:

                error = response.json()

                st.error(
                    error.get(
                        "error",
                        "Something went wrong"
                    )
                )

        except Exception as e:

            st.error(
                f"Connection failed: {e}"
            )


st.divider()


# ---------------------------------
# DISPLAY TODOS
# ---------------------------------

st.subheader("📋 Your Todos")


if not data:

    st.info("No todos found.")

else:

    for todo in data:

        st.write(
            f"**ID:** {todo['id']}  |  "
            f"**Task:** {todo['task']}"
        )

        # Delete
        if st.button(
            "🗑️ Delete",
            key=f"delete_{todo['id']}"
        ):

            try:

                response = requests.delete(
                    f"{API_URL}/todos/{todo['id']}"
                )

                if response.status_code == 200:

                    st.success(
                        "Task deleted!"
                    )

                    st.rerun()

                else:

                    error = response.json()

                    st.error(
                        error.get(
                            "error",
                            "Unable to delete task"
                        )
                    )

            except Exception as e:

                st.error(
                    f"Connection failed: {e}"
                )


        # Edit
        new_task = st.text_input(
            "Edit Task",
            value=todo["task"],
            key=f"text_{todo['id']}"
        )


        completed = st.checkbox(
            "Completed",
            value=todo["completed"],
            key=f"completed_{todo['id']}"
        )


        # Update
        if st.button(
            "✏️ Update",
            key=f"edit_{todo['id']}"
        ):

            if not new_task.strip():

                st.warning(
                    "Task cannot be empty."
                )

            else:

                try:

                    response = requests.put(
                        f"{API_URL}/todos/{todo['id']}",
                        json={
                            "task": new_task,
                            "completed": completed
                        }
                    )

                    if response.status_code == 200:

                        st.success(
                            "Task updated!"
                        )

                        st.rerun()

                    else:

                        error = response.json()

                        st.error(
                            error.get(
                                "error",
                                "Task not updated"
                            )
                        )

                except Exception as e:

                    st.error(
                        f"Connection failed: {e}"
                    )

        st.divider()