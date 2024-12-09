function addSubtaskDeleteEvent(button, subtaskList, subtaskContainer){
    button.addEventListener('click', function(e) {
        e.preventDefault()
    subtaskId = this.getAttribute("data-id");

    fetch(`/delete-subtask/${subtaskId}`, {
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
        
        if (subtaskList.children.length===0){
            subtaskContainer.hidden = true;
        }

        }
    })
    .catch(error => console.log("Error:", error));
    });
}

function addSubmitAddSubtaskEvent(){
    addSubtaskForm.addEventListener('submit', function (e){
        e.preventDefault();

        const formData = new FormData(addSubtaskForm);
        const url = addSubtaskForm.getAttribute('data-url');

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
                        <button class = "edit-subtask-btn small-subtask-button" data-id = "${subtask.id}" data-url = "/edit/${subtask.to_do}/"><i class="fas fa-edit"></i></button>
                        <button class = "delete-subtask-btn small-subtask-button" data-id = "${subtask.id}"><i class="fas fa-trash"></i></button>
                        </div>
                    </div>
                    <p>${subtask.text}</p>
                    <br>
                    <input type="checkbox" name ="completed" ${subtask.completion ? 'checked' :""}>
                    <label for = "completed">Completed</label>
                    <hr>
                    <br>
                </div>
                `;

                subtaskList.insertAdjacentHTML('beforeend', subtaskItem);
                subtaskContainer.hidden = false;
                addSubtaskForm.reset();

                const deleteButton = document.querySelector(`#subtask-${subtask.id} .delete-subtask-btn`);
                const editButton = document.querySelector(`#subtask-${subtask.id} .edit-subtask-btn`);
                addSubtaskDeleteEvent(deleteButton, subtaskList, subtaskContainer);
                addEditSubtaskEvent(editButton);

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
}

function addEditSubtaskEvent(button){
    button.addEventListener('click', function(e) {
    e.preventDefault();             
    const formContainer =document.getElementById('form-container');
    const formPosition = formContainer.getBoundingClientRect().top + window.scrollY;
    const addSubtaskHTML = formContainer.innerHTML;
    const subtaskId = this.getAttribute("data-id");
    const subtaskContainer = document.getElementById(`subtask-${subtaskId}`)
    const subtaskPosition = subtaskContainer.getBoundingClientRect().top + window.scrollY;
    const subtaskTitle = subtaskContainer.querySelector('h4');
    const subtaskText = subtaskContainer.querySelector('p');
    const subtaskTitleContent = subtaskTitle?.textContent || "";
    const subtaskTextContent = subtaskText?.textContent || "";
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || getCookie('csrftoken');
    const subtaskCompletion = subtaskContainer.querySelector('input["type"]=checkbox')?.checked || false;


    const editSubtaskHtml = `
    <h2 id="form">Edit subtask:</h2>
    <form data-url="/update-subtask/${subtaskId}" method="post" id="saveEditedSubtaskForm">
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
        <label for="title">Title:</label>
        <input type="text" id="title" name="title" placeholder="Title" value = "${subtaskTitleContent}" required>
        <label for="text">Description:</label>
        <textarea id="text" name="text" rows="4" placeholder="Description" required>${subtaskTextContent}</textarea>
        <br>
        <div class = "completed-div">
        <input type="checkbox" id="completion" name="completion" ${subtaskCompletion ? 'checked' : ''}>
        <label for = "completed">Completed</label>
        </div>
        <br>
        <button type = 'submit' data-url="/update-subtask/${subtaskId}" >Save</button>
    </form>`
    window.scrollTo({
        top: formPosition,
        behavior: 'smooth'
    });

    formContainer.innerHTML = editSubtaskHtml;
    const saveEditedSubtaskForm = formContainer.querySelector("form")

    
    
    saveEditedSubtaskForm.addEventListener("submit", function(e) {
        e.preventDefault();

        const formData = new FormData(saveEditedSubtaskForm);
        const dataUrl = this.getAttribute("data-url")

        fetch(dataUrl, {
            method:"POST",
            headers: {
                'X-CSRFToken':document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: formData

        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status==="success"){
                const subtask = data.subtask;

                subtaskTitle.textContent = subtask.title;
                subtaskText.textContent = subtask.text;
                formContainer.innerHTML = addSubtaskHTML;

                window.scrollTo({
                    top: subtaskPosition,
                    behavior: 'smooth'
                });


            };
        });

    });

    addEditSubtaskEvent();
});}

document.addEventListener('DOMContentLoaded', function () {  
    const currentUrl = window.location.pathname;
    const addSubtaskForm = document.getElementById("subtask-form");
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
            const completionTime = document.getElementById(`completion-date-${todoId}`);

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
                    if (data.completion) {
                        completionTime.textContent = data.completion_date;
                        completionTime.hidden = false;
                    } 
                    else {
                        completionTime.hidden = true;
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

    if (currentUrl.includes('details')){
        addSubmitAddSubtaskEvent();
        addSubtaskForm.addEventListener('submit', function (e){
            e.preventDefault();

            const formData = new FormData(addSubtaskForm);
            const url = addSubtaskForm.getAttribute('data-url');

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
                            <button class = "edit-subtask-btn small-subtask-button" data-id = "${subtask.id}" data-url = "/edit/${subtask.to_do}/"><i class="fas fa-edit"></i></button>
                            <button class = "delete-subtask-btn small-subtask-button" data-id = "${subtask.id}"><i class="fas fa-trash"></i></button>
                            </div>
                        </div>
                        <p>${subtask.text}</p>
                        <br>
                        <input type="checkbox" name ="completed" ${subtask.completion ? 'checked' :""}>
                        <label for = "completed">Completed</label>
                        <hr>
                        <br>
                    </div>
                    `;

                    subtaskList.insertAdjacentHTML('beforeend', subtaskItem);
                    subtaskContainer.hidden = false;
                    addSubtaskForm.reset();

                    const deleteButton = document.querySelector(`#subtask-${subtask.id} .delete-subtask-btn`);
                    const editButton = document.querySelector(`#subtask-${subtask.id} .edit-subtask-btn`);
                    addSubtaskDeleteEvent(deleteButton, subtaskList, subtaskContainer);
                    addEditSubtaskEvent(editButton);

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

        document.querySelectorAll('.delete-subtask-btn').forEach(
            button => addSubtaskDeleteEvent(button, subtaskList, subtaskContainer)
        );

        document.querySelectorAll('.edit-subtask-btn').forEach(
        button => { addEditSubtaskEvent(button)
        });
    };

    

    

});