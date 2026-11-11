function showFolderForm() {
    document.getElementById("folder-form").style.display = "block";
}

function showDeleteButton(button) {
    // Find the parent <li> containing the clicked button
    const folder = button.closest('li');

    // Find the confirmation box inside that folder
    const confirmBox = folder.querySelector('.folder-delete-confirm');

    // Display the confirmation box
    confirmBox.style.display = 'block';
}

function showDeleteTaskButton(button) {
    // Find the parent <li> containing the clicked button
    const task = button.closest('li');

    // Find the confirmation box inside that folder
    const confirmBox = task.querySelector('.task-delete-confirm');

    // Display the confirmation box
    confirmBox.style.display = 'block';
}

function cancelDelete(button) {
    const folder = button.closest('li');
    const confirmBox = folder.querySelector('.folder-delete-confirm');

    confirmBox.style.display = 'none';
}

function cancelDeleteTask(button) {
    const task = button.closest('li');
    const confirmBox = task.querySelector('.task-delete-confirm');

    confirmBox.style.display = 'none';
}

function deleteFolder(button) {
    const folder = button.closest('li');
    const folderId = folder.dataset.folderId;

    fetch('/delete-folder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ folder_id: folderId })
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        }
    });
}

function deleteTask(button) {
    const task = button.closest('li');
    const taskId = task.dataset.taskId;

    fetch('/delete-task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task_id: taskId })
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        }
    });
}

function selectFolder(button) {
    const folder = button.closest('li');
    const folderId = folder.dataset.folderId;

    window.location.href = `/?folder_id=${encodeURIComponent(folderId)}`;
}

function toggleTask(checkbox) {
    const taskId = checkbox.closest('li').dataset.taskId;
    const isDone = checkbox.checked;

    fetch('/toggle-task', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            task_id: taskId,
            is_done: isDone
        })
    });
}