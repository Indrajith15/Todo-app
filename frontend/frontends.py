import streamlit as st
import requests
st.title("My Todo App")
#displaying task
try:
    data=[]
    response = requests.get("http://localhost:5000/todos")
    if response.status_code == 200:
        data=response.json()
        for todo in data:
            st.write(f"Id:{todo['id']}, Task:{todo['task']}")
    else:
        st.error("Unable to fetch todos")
except Exception as e:
    st.error(f"Connection Failed:{e}")

#inseting tasks
try:
        task = st.text_input("Enter the task:")
        if st.button("Add Task"):
            response = requests.post("http://localhost:5000/todos",
                                     json = {
                                         "task": task
                                     })
            if response.status_code == 200:
                data = response.json()
                st.success(data["message"])
                st.rerun()
            else:
                st.error("Something went wrong")
except Exception as e:
     st.error(f"Connection failed: {e}")

#deleting task
for todo in data:
     st.write(todo["task"])
     if st.button("Delete",key=f"delete_{todo['id']}"):
        response = requests.delete(f"http://localhost:5000/todos/{todo['id']}")
        if response.status_code == 200:
            st.success("Task deleted")
            st.rerun()
        else:
              st.error("Unable to delete task")

#updating task
     st.write(todo["task"])
     new_task = st.text_input("Edit Task", value = todo["task"],key=f"text_{todo['id']}")
     if st.button("Update", key= f"edit_{todo['id']}"):
          response = requests.put(f"http://localhost:5000/todos/{todo['id']}",
                                  json = {"task": new_task})
          if response.status_code == 200:
               data= response.json()
               st.success(data['message'])
               st.rerun()
          else:
               st.error("Task not updated")
          
               

     



