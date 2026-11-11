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

function cancelDelete(button) {
    const folder = button.closest('li');
    const confirmBox = folder.querySelector('.folder-delete-confirm');

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