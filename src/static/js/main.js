const sidebarIds = ['seamless', 'wang', 'pixel', 'procedural', 'colours'];
const detailsId = ['brick', 'brickborder', 'noise'];
const OPERATIONS = {
    "SEAMLESS": {
        fn: async function(file) {
            const formData = new FormData();
            formData.append('image', dataBuffers[file]);
            formData.append('use_best', 'false');

            await fetchCommand('/seamless', formData, file);
        },
    },
    "CROP_IMAGE": {
        fn: async function(file) {
            const formData = new FormData();
            formData.append('image', dataBuffers[file]);
            formData.append('tile_width', document.getElementById('tileWidth').value);
            formData.append('tile_height', document.getElementById('tileHeight').value);

            await fetchCommand('/seamless', formData, file);
        },
    },
    "UPLOAD": {
        fn: async function(file) {
            const formData = new FormData();
            formData.append('image', dataBuffers[file]);
            formData.append('num_colours', document.getElementById('numColours').value);
            formData.append('pixel_size', document.getElementById('pixelSize').value);

            await fetchCommand('/upload', formData, file);
        },
    },
    "COLOUR_SHIFT": {
        fn: async function(file) {
            const formData = new FormData();
            formData.append('image', dataBuffers[file]);
            formData.append('red_shift', document.getElementById('redShift').value);
            formData.append('green_shift', document.getElementById('greenShift').value);
            formData.append('blue_shift', document.getElementById('blueShift').value);
            formData.append('filename', file);

            await fetchCommand('/colour_shift', formData, file);
        },
    },
    "PROCEDURAL": {
        fn: async function(file) {
            const formData = new FormData();
            
            const texture_type =  document.getElementById('textureOption').value;
            formData.append('texture_type', texture_type);
            if (texture_type == 'brick')  {
                formData.append('brick_width', document.getElementById('brickWidth').value);
                formData.append('brick_height', document.getElementById('brickHeight').value);
                formData.append('mortar_size', document.getElementById('mortarSize').value);
                formData.append('mortar_colour', document.getElementById('mortarChosenColour').value);
                formData.append('threshold', document.getElementById('brickColourThreshold').value);
            } else if (texture_type == 'noise') {
                formData.append('threshold_1', document.getElementById('colour1Threshold').value);
                formData.append('threshold_2', document.getElementById('colour2Threshold').value);
                formData.append('threshold_3', document.getElementById('colour3Threshold').value);
                formData.append('threshold_4', document.getElementById('colour4Threshold').value);
                formData.append('threshold_5', document.getElementById('colour5Threshold').value);
            }
            
            formData.append('tile_width', document.getElementById('noiseWidth').value);
            formData.append('tile_height', document.getElementById('noiseHeight').value);
            formData.append('base_frequency', document.getElementById('baseFrequency').value);
            formData.append('cell_size', document.getElementById('cellSize').value);
            formData.append('noise_octaves', document.getElementById('noiseOctaves').value);
            formData.append('noise_persistance', document.getElementById('noisePersistance').value);
            formData.append('noise_lacunarity', document.getElementById('noiseLacunarity').value);

            palette_mode = document.getElementById('paletteNoise').value;
            val = document.getElementById('noiseChosenColour').value;
            val = val.toUpperCase();
            chosen_colour = val.slice(1);

            const url = 'https://www.thecolorapi.com/scheme?hex='+chosen_colour+'&format=json&mode='+palette_mode+'&count=5';
            const palette = await colourPaletteFetch(url);
            formData.append('colours', palette);

            await fetchCommand('/procedural', formData, file);
        },
    },
    "NEAREST_NEIGHBOUR": {
        fn: async function(file) {
            pixel_size = document.getElementById('pixelSize').value;
            rounded_width = Math.round(img_width/pixel_size);
            rounded_height = Math.round(img_height/pixel_size);

            const formData = new FormData();
            formData.append('image', dataBuffers[file]);
            formData.append('width', rounded_width);
            formData.append('height', rounded_height);

            await fetchCommand('/nearest_neighbour', formData, file);
        },
    },
    "WANG_TILES": {
        fn: async function(file) {
            const formData = new FormData();
            formData.append('image', dataBuffers[file]);

            await fetchCommand('/wang_tiles', formData, file);
        },
    },
    "WANG_BORDERS": {
        fn: async function(file) {
            const formData = new FormData();
            formData.append('image', dataBuffers[file]);
            formData.append('width', img_width);
            formData.append('height', img_height);
            formData.append('border_size', document.getElementById('borderSize').value);

            border_style =  document.getElementById('borderStyle').value;
            formData.append('border_style', border_style);

            if (border_style == 'brickborder') {
                formData.append('brick_border_width', document.getElementById('brickBorderWidth').value);
                formData.append('brick_border_height', document.getElementById('brickBorderHeight').value);
                formData.append('mortar_border', document.getElementById('mortarBorder').value);
            } else if (border_style == 'noise') {
                formData.append('base_frequency', document.getElementById('baseFrequency').value);
                formData.append('cell_size', document.getElementById('cellSize').value);
                formData.append('noise_octaves', document.getElementById('noiseOctaves').value);
                formData.append('noise_persistance', document.getElementById('noisePersistance').value);
                formData.append('noise_lacunarity', document.getElementById('noiseLacunarity').value);

                formData.append('threshold_1', document.getElementById('colour1Threshold').value);
                formData.append('threshold_2', document.getElementById('colour2Threshold').value);
                formData.append('threshold_3', document.getElementById('colour3Threshold').value);
                formData.append('threshold_4', document.getElementById('colour4Threshold').value);
                formData.append('threshold_5', document.getElementById('colour5Threshold').value);

                palette_mode = document.getElementById('paletteNoise').value;
                val = document.getElementById('noiseChosenColour').value;
                val = val.toUpperCase();
                chosen_colour = val.slice(1);

                const url = 'https://www.thecolorapi.com/scheme?hex='+chosen_colour+'&format=json&mode='+palette_mode+'&count=5';
                const palette = await colourPaletteFetch(url);
                formData.append('colours', palette);
            } else if (border_style == "noise_mask") {
                formData.append('base_frequency', document.getElementById('baseFrequency').value);
                formData.append('cell_size', document.getElementById('cellSize').value);
                formData.append('noise_octaves', document.getElementById('noiseOctaves').value);
                formData.append('noise_persistance', document.getElementById('noisePersistance').value);
                formData.append('noise_lacunarity', document.getElementById('noiseLacunarity').value);
            }

            await fetchCommand('/wang_borders', formData, file);
        },
    },
    "COLOUR_PALETTE": {
        fn: async function(file) {
            palette_mode = document.getElementById('paletteMode').value;
            val = document.getElementById('chosenColour').value;
            val = val.toUpperCase();
            chosen_colour = val.slice(1);

            const url = 'https://www.thecolorapi.com/scheme?hex='+chosen_colour+'&format=json&mode='+palette_mode+'&count=6';

            const palette = await colourPaletteFetch(url);

            const formData = new FormData();
            formData.append('image', dataBuffers[file]);
            formData.append('colours', palette);
            formData.append('factor', document.getElementById('paletteFactor').value);

            await fetchCommand('/colour_palette', formData, file);
        },
    },
}

// key is filename and value is file/blob or image data
let activeFiles = {};
let dataBuffers = {};

// current array of OPERATIONs to chain together
let workQueue = [];

let awaitingCompletion = [];
let img_width, img_height = 0

function toggleDetails(activeId) {
    detailsId.forEach(id => {
        const details = document.getElementById(`${id}-details`);
        details.style.display = id === activeId ? 'block' : 'none';
    });
}

document.getElementById('textureOption').addEventListener('change', function(event) {
   toggleDetails(event.target.value);
});

document.getElementById('borderStyle').addEventListener('change', function(event) {
    toggleDetails(event.target.value);
 });

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

// helper function to convert file/blob objects to base64 strings
async function blobToBase64(blob) {
  return new Promise((resolve, _) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.readAsDataURL(blob);
  });
}

// helper function to convert base64 string data to blob objects
function base64ToBlob(base64, mime) 
{
    mime = mime || '';
    var sliceSize = 1024;
    var byteChars = window.atob(base64);
    var byteArrays = [];

    for (var offset = 0, len = byteChars.length; offset < len; offset += sliceSize) {
        var slice = byteChars.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

    return new Blob(byteArrays, {type: mime});
}

// copies data from activeFiles to dataBuffers for processing
function initDataBuffers() {
    let file;
    dataBuffers = {};
    for (file in activeFiles) {
        awaitingCompletion.push(file);
        dataBuffers[file] = base64ToBlob(activeFiles[file].replace(/^data:image\/(png|jpeg);base64,/, "") , 'image/png');
    }
}

// dispatches work queues for all images
function dispatchWorkQueues() {
    document.getElementById("outputImage").innerHTML = "";
    document.getElementById("outputPreviewContainer").innerHTML = "";
    awaitingCompletion = [];
    initDataBuffers();
    let file;
    for (file in dataBuffers) {
        processWorkQueue(file, workQueue);
    }
}

// helper that focuses on all work ops for a single image
async function processWorkQueue(file, operations) {
    let op;
    let fn;
    for ( op of operations ) {
        if (!(op in OPERATIONS)) {
            console.error("op [" + op + "] not defined in OPERATIONS table!");
            continue;
        }

        console.log(file, op);

        fn = OPERATIONS[op].fn;
        await fn(file);
    }

    let idx = awaitingCompletion.indexOf(file);
    if( idx !== -1 ) {
        awaitingCompletion.splice(idx, 1);
    }

    if (awaitingCompletion.length === 0) {
        loader.style.display = 'none';
    }

    if (document.getElementById("outputImage").innerHTML === "") {
        await fileReader(dataBuffers[file], 'outputDisplay', 'outputImage', 64, false);
    }

    await fileReader(dataBuffers[file], `output-${file}`, 'outputPreviewContainer', 64, false);
}

// removes active selection from all elements
function clearActiveSelections() {
    let elements = document.querySelectorAll('.active-selection');
    for(let elem of elements) {
        elem.classList.remove('active-selection');
    };
}

// adds border to both input/output image containers
function onPreviewClicked(event) {
    let target = event.target;
    clearActiveSelections()
    let focusedFile = target.getAttribute('data-filename');

    if (focusedFile in activeFiles) {
        document.querySelector("#imageContainer > img").src = activeFiles[focusedFile];
        document.getElementById(focusedFile).classList.add('active-selection');
    }

    if (focusedFile in dataBuffers) {
        document.querySelector("#outputImage > img").src = dataBuffers[focusedFile];
        document.getElementById(`output-${focusedFile}`).classList.add('active-selection');
    }
}

// post-parse reader
//
// readerData: base64 image information
// filename: name of file
// img_id: id of image container we will create
// div_id: id of container to add the new image to
// customDims: custom image dims (width and height)
// clearPrevious: if the container with id div_id should be cleared
async function onFileRead(readerData, filename, img_id, div_id, customDims, clearPrevious) {
    const img = document.createElement('img');
    if (img_id.includes("output")) {
        dataBuffers[filename] = readerData;
        img.src = dataBuffers[filename];
    } else {
        activeFiles[filename] = readerData;
        img.src = activeFiles[filename];
    }
    img.id = img_id;
    const container = document.getElementById(div_id);
    if (clearPrevious) {
        container.innerHTML = ''; // Clear previous image
    }
    container.appendChild(img);
    if (div_id == 'imageContainer') {
        img.className = "pure-img";
        img.onload = function() {
            pixel_size = document.getElementById('pixelSize').value;
            img_width = this.naturalWidth;
            img_height = this.naturalHeight;
            rounded_width = Math.round(img_width/pixel_size);
            rounded_height = Math.round(img_height/pixel_size);
            document.getElementById('dimensions-label').innerHTML = `${rounded_width}x${rounded_height}`;
        }
    } else if (div_id == "inputPreviewContainer" || div_id == "outputPreviewContainer") {
        img.alt = filename;
        img.setAttribute("data-filename", filename);
        img.setAttribute("data-container", div_id == "inputPreviewContainer" ? "#imageContainer > img" : "#outputImage > img");
        let clampedDim = customDims <= 0 ? 64 : customDims;
        img.width = clampedDim;
        img.height = clampedDim;
        img.addEventListener('click', onPreviewClicked);
    }
}

// converts image information to base64 if needed and passes it to the onFileRead for rendering
//
// file: the base64, Blob, or File of the image to read
// img_id: passthrough parameter for onFileRead
// div_id: passthrough
// customDims: passthrough
// clearPrevious: passthrough
async function fileReader(file, img_id, div_id, customDims = -1, clearPrevious = true) {
    let filename = file instanceof File ? file.name : img_id.replace("output-", "");
    let readResult = file instanceof Blob ? await blobToBase64(file) : file;
    await onFileRead(readResult, filename, img_id, div_id, customDims, clearPrevious)
}

// clears imageContainer if data is null, otherwise focuses on the provided image
async function updateSelectedFile(data) {
    if (!data) {
        document.getElementById("imageContainer").innerHTML = "";
        return;
    }

    if (  !(data.name in activeFiles)) {
        await fileReader(data, 'uploadedImage', 'imageContainer');
        return;
    }
}

// redraws preview carriages
function redrawPreviews(clearPrevious, forOutput = false) {
    let previewsContainer = forOutput ? "outputPreviewContainer" : "inputPreviewContainer";
    let previewFocusContainer = forOutput ? "outputImage" : "imageContainer";
    let dataSource = forOutput ? dataBuffers : activeFiles;

    if (clearPrevious) {
        document.getElementById(previewsContainer).innerHTML = "";
        document.getElementById(previewFocusContainer).innerHTML = "";
    }

    for (file in dataSource) {
        if (document.getElementById(previewFocusContainer).innerHTML === "") {
            fileReader(dataSource[file], file, previewFocusContainer, -1, false);
        }
        fileReader(dataSource[file], file, previewsContainer, -1, false);
    }
}

document.getElementById('imageClear').addEventListener('click', function(event) {
    inputPreviewContainer.innerHTML = '';
    imageInputForm.reset();
    updateSelectedFile(null);
    activeFiles = {};
});

document.getElementById('imageUpload').addEventListener('change', async function(event) {
    inputPreviewContainer.innerHTML = '';
    imageClear.classList.remove('hidden');
    clearActiveSelections();

    let fileCt = event.target.files.length;
    let i;
    for(i = 0; i < fileCt; ++i) {
        activeFiles[event.target.files[i].name] = await blobToBase64(event.target.files[i]);
    }

    redrawPreviews(false);
});

document.getElementById("setOutputAsInput").addEventListener('click', function() {
    imageClear.click()
    for (file in dataBuffers) {
        activeFiles[file] = dataBuffers[file];
    }
    redrawPreviews(false);
});

document.getElementById("makeSeamless").addEventListener('click', function() {
    workQueue = ["SEAMLESS"];
    dispatchWorkQueues();
});

document.getElementById('cropImage').addEventListener('click', function(event) {
    workQueue = ["CROP_IMAGE"];
    dispatchWorkQueues();
});

document.getElementById('uploadButton').addEventListener('click', function(event) {
    workQueue = ["UPLOAD"];
    dispatchWorkQueues();
});

document.getElementById('colourShift').addEventListener('click', function(event) {
    workQueue = ["COLOUR_SHIFT"];
    dispatchWorkQueues();
});

document.getElementById('generateNoise').addEventListener('click', async function(event) {
    workQueue = ["PROCEDURAL"];
    dispatchWorkQueues();
});

document.getElementById('pixelSize').addEventListener('change', function(event) {
    pixel_size = document.getElementById('pixelSize').value;
    rounded_width = Math.round(img_width/pixel_size);
    rounded_height = Math.round(img_height/pixel_size);
    document.getElementById('dimensions-label').innerHTML = `${rounded_width}x${rounded_height}`;
});

document.getElementById('scaleDown').addEventListener('click', function(event) {
    workQueue = ["NEAREST_NEIGHBOUR"];
    dispatchWorkQueues();
});

document.getElementById('wangTiles').addEventListener('click', function(event) {
    workQueue = ["WANG_TILES"];
    dispatchWorkQueues();
});

document.getElementById('wangBorders').addEventListener('click', async function(event) {
    workQueue = ["WANG_BORDERS"];
    dispatchWorkQueues();
});

document.getElementById('colourPalette').addEventListener('click', async function(event) {
    workQueue = ["COLOUR_PALETTE"];
    dispatchWorkQueues();
});

document.getElementById('uploadAndScale').addEventListener('click', async function(event) {
    workQueue = ["UPLOAD", "NEAREST_NEIGHBOUR"];
    dispatchWorkQueues();
});

async function colourPaletteFetch(url) {
    palette = []
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const col = data.colors;

        for (let i = 0; i < col.length; i++) {
            palette.push([
              col[i].rgb.r,
              col[i].rgb.g,
              col[i].rgb.b
            ]);
        }

        return JSON.stringify(palette);
    } catch (error) {
        throw error;
    }
}

async function fetchCommand(route_name, formData, filename) {
    loader = document.getElementById('loader');
    loader.style.display = 'block';

    let res = await fetch(route_name, {
        method: 'POST',
        body: formData,
    });

    if( !res.ok ) {
        console.error('Error:', await res.text());
        document.getElementById('outputImage').textContent = 'An error occurred during upload.';
        return;
    }

    dataBuffers[filename] = await res.blob();
}
