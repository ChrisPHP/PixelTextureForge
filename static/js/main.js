document.addEventListener("DOMContentLoaded", () => {
    let selectedFile = null;

    document.getElementById('imageUpload').addEventListener('change', function(event) {
        selectedFile = event.target.files[0];
        if (selectedFile) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.id = 'uploadedImage';
                const container = document.getElementById('imageContainer');
                container.innerHTML = ''; // Clear previous image
                container.appendChild(img);
            }
            reader.readAsDataURL(selectedFile);
        }
    });

    document.getElementById("uploadButton").addEventListener('click', function(event) {
        if (selectedFile) {
            const formData = new FormData();
            formData.append('image', selectedFile);
            formData.append('num_colours', document.getElementById('numColours').value);
            formData.append('pixel_size', document.getElementById('pixelSize').value);

            fetch('/upload', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.blob())
            .then(blob => {
                const img = document.createElement('img');
                img.src = URL.createObjectURL(blob);
                img.id = 'uploadedImage';
                const container = document.getElementById('outputImage');
                container.innerHTML = ''; // Clear previous image
                container.appendChild(img);
                //document.getElementById('outputImage').textContent = 'Image uploaded and displayed successfully!';
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('outputImage').textContent = 'An error occurred during upload.';
            });
        }
        
    });
});
