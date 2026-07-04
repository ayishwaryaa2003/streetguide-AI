import { processImage } from "./js/api.js";

const imageInput = document.getElementById("imageInput");
const previewImage = document.getElementById("previewImage");
const dropZone = document.getElementById("dropZone");

const translateBtn = document.getElementById("translateBtn");

const sourceLanguage = document.getElementById("sourceLanguage");
const targetLanguage = document.getElementById("targetLanguage");

const visionStatus = document.getElementById("visionStatus");
const textStatus = document.getElementById("textStatus");
const navigationStatus = document.getElementById("navigationStatus");

const ocrOutput = document.getElementById("ocrOutput");
const translatedOutput = document.getElementById("translatedOutput");
const navigationOutput = document.getElementById("navigationOutput");

function updateStatus(element, state) {

    element.className = "status";

    switch (state) {

        case "waiting":
            element.classList.add("waiting");
            element.textContent = "Waiting";
            break;

        case "processing":
            element.classList.add("processing");
            element.textContent = "Processing...";
            break;

        case "completed":
            element.classList.add("completed");
            element.textContent = "Completed";
            break;

        case "error":
            element.classList.add("error");
            element.textContent = "Error";
            break;
    }
}

function resetUI() {

    updateStatus(visionStatus, "waiting");
    updateStatus(textStatus, "waiting");
    updateStatus(navigationStatus, "waiting");

    ocrOutput.textContent = "Waiting for processing...";
    translatedOutput.textContent = "Waiting for processing...";
    navigationOutput.textContent = "Waiting for processing...";
}

function showPreview(file) {

    previewImage.src = URL.createObjectURL(file);
    previewImage.style.display = "block";

    document.getElementById("fileName").textContent =
        "📄 " + file.name;

    document.getElementById("fileSize").textContent =
        "💾 " + (file.size / 1024 / 1024).toFixed(2) + " MB";

    const img = new Image();

    img.onload = () => {

        document.getElementById("fileResolution").textContent =
            "🖼 " + img.width + " × " + img.height;

    };

    img.src = URL.createObjectURL(file);
}

imageInput.addEventListener("change", () => {

    if (imageInput.files.length) {

        showPreview(imageInput.files[0]);

    }

});

dropZone.addEventListener("dragover", (e) => {

    e.preventDefault();

    dropZone.classList.add("drag-over");

});

dropZone.addEventListener("dragleave", () => {

    dropZone.classList.remove("drag-over");

});

dropZone.addEventListener("drop", (e) => {

    e.preventDefault();

    dropZone.classList.remove("drag-over");

    const file = e.dataTransfer.files[0];

    if (!file) return;

    imageInput.files = e.dataTransfer.files;

    showPreview(file);

});

translateBtn.addEventListener("click", async () => {

    if (!imageInput.files.length) {

        alert("Please upload an image.");

        return;
    }

    resetUI();

    updateStatus(visionStatus, "processing");
    updateStatus(textStatus, "processing");
    updateStatus(navigationStatus, "processing");

    const formData = new FormData();

    formData.append("image", imageInput.files[0]);

    formData.append(
        "source_language",
        sourceLanguage.value
    );

    formData.append(
        "target_language",
        targetLanguage.value
    );

    try {

        const result = await processImage(formData);

        updateStatus(visionStatus, "completed");
        updateStatus(textStatus, "completed");
        updateStatus(navigationStatus, "completed");

        ocrOutput.textContent =
            result.ocr_text || "No OCR text";

        translatedOutput.textContent =
            result.transliterated_text || "No transliteration";

        navigationOutput.textContent =
            result.navigation || "No navigation guidance";

    }
    catch (error) {

        console.error(error);

        updateStatus(visionStatus, "error");
        updateStatus(textStatus, "error");
        updateStatus(navigationStatus, "error");

        navigationOutput.textContent =
            error.message;

    }

});