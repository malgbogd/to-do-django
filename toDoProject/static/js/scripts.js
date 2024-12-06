document.addEventListener('DOMContentLoaded', function () {  
    const currentUrl = window.location.pathname;
    
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
                    if (data.status == 'success') {
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


});