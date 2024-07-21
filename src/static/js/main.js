document.addEventListener("DOMContentLoaded", () => {
    // Header Buttons

    const sidebarIds = ['seamless', 'wang', 'pixel', 'procedural', 'colours'];

    function toggleSidebar(activeId) {
        sidebarIds.forEach(id => {
            const sidebar = document.getElementById(`${id}-sidebar`);
            sidebar.style.display = id === activeId ? 'block' : 'none';
        });
    }

    sidebarIds.forEach(id => {
        const menuOpen = document.getElementById(`${id}-menu-open`);
        menuOpen.addEventListener('click', () => toggleSidebar(id));
    });

    let selectedFile = null
    let outputFile = null
    let img_width, img_height = 0

    function file_reader(file, img_id, div_id) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.id = img_id;
            const container = document.getElementById(div_id);
            container.innerHTML = ''; // Clear previous image
            container.appendChild(img);
            if (div_id == 'imageContainer') {
                img.onload = function() {
                    pixel_size = document.getElementById('pixelSize').value;
                    img_width = this.naturalWidth;
                    img_height = this.naturalHeight;
                    rounded_width = Math.round(img_width/pixel_size);
                    rounded_height = Math.round(img_height/pixel_size);
                    document.getElementById('dimensions-label').innerHTML = `${rounded_width}x${rounded_height}`;
                }
            }
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

    document.getElementById('colourShift').addEventListener('click', function(event) {
        if (selectedFile) {
            const formData = new FormData();
            formData.append('image', selectedFile);
            formData.append('red_shift', document.getElementById('redShift').value)
            formData.append('green_shift', document.getElementById('greenShift').value)
            formData.append('blue_shift', document.getElementById('blueShift').value)

            fetch_command('/colour_shift', formData);
        }
    });

    document.getElementById('generateNoise').addEventListener('click', function(event) {
        const formData = new FormData();
        formData.append('base_frequency', document.getElementById('baseFrequency').value);
        formData.append('cell_size', document.getElementById('cellSize').value);
        formData.append('noise_octaves', document.getElementById('noiseOctaves').value);
        formData.append('noise_persistance', document.getElementById('noisePersistance').value);
        formData.append('noise_lacunarity', document.getElementById('noiseLacunarity').value);

        fetch_command('/procedural', formData);
    });

    document.getElementById('pixelSize').addEventListener('change', function(event) {
        pixel_size = document.getElementById('pixelSize').value;
        rounded_width = Math.round(img_width/pixel_size);
        rounded_height = Math.round(img_height/pixel_size);
        document.getElementById('dimensions-label').innerHTML = `${rounded_width}x${rounded_height}`;
    });

    document.getElementById('scaleDown').addEventListener('click', function(event) {        
        pixel_size = document.getElementById('pixelSize').value;
        rounded_width = Math.round(img_width/pixel_size);
        rounded_height = Math.round(img_height/pixel_size);

        const formData = new FormData();
        formData.append('image', selectedFile);
        formData.append('width', rounded_width);
        formData.append('height', rounded_height);

        fetch_command('/nearest_neighbour', formData);
    });

    document.getElementById('wangTiles').addEventListener('click', function(event) {        
        const formData = new FormData();
        formData.append('image', selectedFile);

        fetch_command('/wang_tiles', formData);
    });

    document.getElementById('wangBorders').addEventListener('click', function(event) {        
        const formData = new FormData();
        formData.append('image', selectedFile);
        formData.append('width', img_width);
        formData.append('height', img_height);
        formData.append('border_size', document.getElementById('borderSize').value);
        formData.append('border_style', document.getElementById('borderStyle').value);

        fetch_command('/wang_borders', formData);
    });

    document.getElementById('colourPalette').addEventListener('click', function(event) {        
        palette_mode = document.getElementById('paletteMode').value;
        val = document.getElementById('chosenColour').value;
        val = val.toUpperCase();
        chosen_colour = val.slice(1);

        const url = 'https://www.thecolorapi.com/scheme?hex='+chosen_colour+'&format=json&mode='+palette_mode+'&count=6';

        palette = []

        fetch(url)
        .then(response => {
            if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            col = data.colors;
            for (var i = 0; i < col.length; i++) {
                palette.push([
                    col[i].rgb.r,
                    col[i].rgb.g,
                    col[i].rgb.b
                ]);
            }

            const paletteJSON = JSON.stringify(palette);

            const formData = new FormData();
            formData.append('image', selectedFile);
            formData.append('colours', paletteJSON);
            formData.append('factor', document.getElementById('paletteFactor').value);

            fetch_command('/colour_palette', formData);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    });

    function fetch_command(route_name, formData) {
        fetch(route_name, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.blob())
        .then(blob => {
            if (selectedFile) {
                outputFile = new File([blob], selectedFile.name);
            } else {
                outputFile = new File([blob], 'noise.png');
            }
            file_reader(outputFile, 'uploadedImage', 'outputImage')
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('outputImage').textContent = 'An error occurred during upload.';
        });
    }
});
