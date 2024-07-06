document.addEventListener("DOMContentLoaded", () => {
    // Header Buttons

    document.getElementById('seamless-menu-open').addEventListener('click', function() {
        document.getElementById('seamless-sidebar').style.display = "block";
        document.getElementById('pixel-sidebar').style.display = 'none';
    });

    document.getElementById('pixel-menu-open').addEventListener('click', function() {
        document.getElementById('seamless-sidebar').style.display = "none";
        document.getElementById('pixel-sidebar').style.display = 'block';
    });

    let selectedFile = null
    let outputFile = null

    function file_reader(file, img_id, div_id) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.id = img_id;
            const container = document.getElementById(div_id);
            container.innerHTML = ''; // Clear previous image
            container.appendChild(img);
        }
        reader.readAsDataURL(file);
    }

    document.getElementById('imageUpload').addEventListener('change', function(event) {
        selectedFile = event.target.files[0];
        /*
        loadImage(URL.createObjectURL(selectedFile), (loadedImg) => {
            canvasImg = loadedImg;
            scaleCanvasToImage(loadedImg.width, loadedImg.height);
        });
        */
        if (selectedFile) {
            file_reader(selectedFile, 'uploadedImage', 'imageContainer');
        }
    });

    document.getElementById("setOutputAsInput").addEventListener('click', function() {
        selectedFile = outputFile;
        file_reader(selectedFile, 'uploadedImage', 'imageContainer');
        //document.getElementById('uploadedImage').setAttribute('src', document.getElementById('outputImage').getAttribute('src'));
    });

    document.getElementById("makeSeamless").addEventListener('click', function() {
        if (selectedFile) {
            const formData = new FormData();
            formData.append('image', selectedFile);
            formData.append('use_best', 'false');

            fetch_command('/seamless', formData);
        }  
    });

    document.getElementById('cropImage').addEventListener('click', function(event) {
        if (selectedFile) {
            const formData = new FormData();
            formData.append('image', selectedFile);
            formData.append('tile_width', document.getElementById('tileWidth').value)
            formData.append('tile_height', document.getElementById('tileHeight').value)

            fetch_command('/seamless', formData);
        }
    });

    document.getElementById('uploadButton').addEventListener('click', function(event) {
        if (selectedFile) {
            const formData = new FormData();
            formData.append('image', selectedFile);
            formData.append('num_colours', document.getElementById('numColours').value)
            formData.append('pixel_size', document.getElementById('pixelSize').value)

            fetch_command('/upload', formData);
        }
    });


    function fetch_command(route_name, formData) {
        fetch(route_name, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.blob())
        .then(blob => {
            outputFile = new File([blob], selectedFile.name)
            file_reader(outputFile, 'uploadedImage', 'outputImage')
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('outputImage').textContent = 'An error occurred during upload.';
        });
    }
});
