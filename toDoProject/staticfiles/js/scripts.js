document.addEventListener('DOMContentLoaded', function () {  
    const currentUrl = window.location.pathname;
    const subtaskForm = document.getElementById("subtask-form");
    const subtaskList = document.getElementById("subtasks-list");
    const subtaskContainer = document.getElementById("subtasks-container");
    
    document.querySelectorAll('.delete-button').forEach(
        button => {
            button.addEventListener('click', function () {
                const todoId = this.getAttribute('data-id');
                const redirectUrl = this.getAttribute('data-redirect');

                fetch(`/delete/${todoId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken' :document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },

                    body: `redirect=${encodeURIComponent(redirectUrl)}`
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const todoElement = document.getElementById(`todo-${todoId}`);

                        if (todoElement) {
                            todoElement.remove();
                        }
                    } else if (data.status === 'redirect'){
                        window.location.href = data.url;
                    }
                })
                .catch(error => console.error('Error:', error));
            });
        });


    document.querySelectorAll('.edit-button').forEach(button => {
        button.addEventListener('click', function() {
            const editUrl =this.getAttribute('data-url');
            console.log(editUrl);
            window.location.href = editUrl;
        });
    });

    document.querySelectorAll('.todo-comlition').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const todoId = this.getAttribute('data-id');
            const complitionTime = document.getElementById(`complition-date-${todoId}`);

            fetch(`/check-box-edit/${todoId}/`, {
                method : 'post',
                headers : {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if(data.status === 'success') {
                    if (data.complition) {
                        complitionTime.textContent = data.complition_date;
                        complitionTime.hidden = false;
                    } 
                    else {
                        complitionTime.hidden = true;
                    }
                } else {
                    console.error('Error:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));

            if (currentUrl.includes('edit')) {
                checkbox.disabled = false;
            } else if (checkbox.checked) {
                checkbox.disabled = true;
            }
        });
        
    });

    subtaskForm.addEventListener('submit', function (e){
        e.preventDefault();

        const formData = new FormData(subtaskForm);
        const url = subtaskForm.getAttribute('data-url');

        fetch(url, {
            method: "POST",
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status==="success") {
                const subtask = data.subtask;
                const subtaskItem = `
                <div id="subtask-${subtask.id}">
                    <div class = "to-do-nav">
                        <h4>${subtask.title}</h4>
                        <div class = "to-do-nav">
                        <button class = "small-subtask-button" data-id = "${subtask.id}" data-url = "/edit/${subtask.to_do}/"><i class="fas fa-edit"></i></button>
                        <button class = "delete-subtask-btn small-subtask-button" data-id = "${subtask.id}"><i class="fas fa-trash"></i></button>
                        </div>
                    </div>
                    <p>${subtask.text}</p>
                    <input type="checkbox" name ="completed" ${subtask.complition ? 'checked' :""}>
                    <label for = "completed">Completed</label>
                    <hr>
                    <br>
                </div>
                `;

                subtaskList.insertAdjacentHTML('beforeend', subtaskItem);
                subtaskContainer.hidden = false;
                subtaskForm.reset();




            } else {
                console.error('Error', data.errors);
                alert("Error adding subtask!");
            }
        })
        .catch(error => {
        console.error("error",error);
        alert("Something went wrong")
    })

    })

    document.querySelectorAll('.delete-subtask').forEach(
        button => {
            button.addEventListener('click', function(e) {
                e.preventDefault()
            subtaskId = this.getAttribute("data-id");

            fetch(`/dedelete-subtask/${subtaskId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken' :document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'Content-Type': 'application/x-www-form-urlencoded',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                document.getElementById(`subtask-${subtaskId}`).remove()
                }
            })
            .catch(error => console.log("Error:", error));
            });
        }
    );
});