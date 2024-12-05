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