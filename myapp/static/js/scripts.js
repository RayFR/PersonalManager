// static/js/scripts.js

$(document).ready(function () {
    $('.task a[data-toggle="modal"]').click(function (event) {
        event.preventDefault();
        var url = $(this).data('form-url');
        $.get(url, function (data) {
            $('#modal .modal-content').html(data);
            $('#modal').modal('show');
        });
    });

    $('.delete-task').click(function () {
        var taskId = $(this).data('task-id');
        if (confirm('Are you sure you want to delete this task?')) {
            $.post("/task/delete/" + taskId + "/", {
                csrfmiddlewaretoken: '{{ csrf_token }}'
            }).done(function (data) {
                if (data.success) {
                    location.reload(); // Reload the page to reflect changes
                }
            });
        }
    });
});