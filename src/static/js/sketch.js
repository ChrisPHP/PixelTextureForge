var inputCanvas = null

let canvasImg;
let cropX = 0;
let cropY = 0;
let cropW = 0;
let cropH = 0;
let dragEdge = '';
let edgeThreshold = 10;
let dragStartX, dragStartY;

function setup() {
    inputCanvas = createCanvas(500,500);
    inputCanvas.parent("outputImage");
}
function draw() {
    if (canvasImg) {
        background(220);
        const aspectRatio = canvasImg.width / canvasImg.height;
        let newWidth, newHeight;
    
        if (aspectRatio > 1) {
            newWidth = width;
            newHeight = width / aspectRatio;
        } else {
            newHeight = height;
            newWidth = height * aspectRatio;
        }

        image(canvasImg, (width - newWidth) / 2, (height - newHeight) / 2, newWidth, newHeight);
    
        noFill();
        stroke(255, 0, 0);
        rect(cropX, cropY, cropW, cropH);

        fill(255, 0, 0);
        rect(cropX - 5, cropY - 5, 10, 10);
        rect(cropX + cropW - 5, cropY - 5, 10, 10);
        rect(cropX - 5, cropY + cropH - 5, 10, 10);
        rect(cropX + cropW - 5, cropY + cropH - 5, 10, 10);
    }
}

function mousePressed() {
    if (isOverEdge()) {
        isDragging = true;
    } else if (mouseX > cropX && mouseX < cropX + cropW && mouseY > cropY && mouseY < cropY + cropH) {
        isDragging = true;
        dragEdge = 'move';
        dragStartX = mouseX - cropX;
        dragStartY = mouseY - cropY;
    }
}

function mouseDragged() {
    if (isDragging) {
        if (dragEdge === 'move') {
            let newX = constrain(mouseX - dragStartX, 0, canvasImg.width - cropW);
            let newY = constrain(mouseY - dragStartY, 0, canvasImg.height - cropH);
            cropX = newX;
            cropY = newY;
        } else {
            if (dragEdge.includes('left')) {
                let newX = constrain(mouseX, 0, cropX + cropW);
                cropW += cropX - newX;
                cropX = newX;
            }
            if (dragEdge.includes('right')) {
                cropW = constrain(mouseX, 0, canvasImg.width)
            }
            if (dragEdge.includes('top')) {
                let newY = constrain(mouseY, 0, cropY + cropH);
                cropH += cropY - newY;
                cropY = newY;
            }
            if (dragEdge.includes('bottom')) {
                cropH = constrain(mouseY, 0, canvasImg.height)
            }
        }
    }
}

function scaleCanvasToImage(width, height) {
    cropW = width;
    cropH = height;
    resizeCanvas(width, height);
}

function mouseReleased() {
    isDragging = false;
    dragEdge = '';
}

function isOverEdge() {
    let overLeft = abs(mouseX - cropX) < edgeThreshold;
    let overRight = abs(mouseX - (cropX + cropW)) < edgeThreshold;
    let overTop = abs(mouseY - cropY) < edgeThreshold;
    let overBottom = abs(mouseY - (cropY + cropH)) < edgeThreshold;

    if (overLeft && overTop) dragEdge = 'topleft';
    else if (overRight && overTop) dragEdge = 'topright';
    else if (overLeft && overBottom) dragEdge = 'bottomleft';
    else if (overRight && overBottom) dragEdge = 'bottomright';
    else if (overLeft) dragEdge = 'left';
    else if (overRight) dragEdge = 'right';
    else if (overTop) dragEdge = 'top';
    else if (overBottom) dragEdge = 'bottom';
    else return false;

    return true;
}
