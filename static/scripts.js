document.addEventListener('DOMContentLoaded', () => {
  const dropArea = document.getElementById('drop-area');
  const fileInput = document.getElementById('fileInput');
  const filePreview = document.getElementById('filePreview');

  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
  });

  ['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
  });

  dropArea.addEventListener('drop', handleDrop, false);
  fileInput.addEventListener('change', handleFiles, false);

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function highlight() {
    dropArea.classList.add('highlight');
  }

  function unhighlight() {
    dropArea.classList.remove('highlight');
  }

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
  }

  function handleFiles(files) {
    [...files].forEach(uploadFile);
  }

  function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        const { success, error, filename } = data;
        if (success) {
          const fileReader = new FileReader();
          fileReader.readAsDataURL(file);
          fileReader.onload = () => {
            const img = document.createElement('img');
            img.src = fileReader.result;
            filePreview.appendChild(img);
          };
        } else {
          alert(error);
        }
      })
      .catch(error => {
        alert('An error occurred while uploading the file.');
        console.error('Error:', error);
      });
  }
});
