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

    translateBtn.disabled = true;
    translateBtn.textContent = "⏳ Processing...";

    updateStatus(visionStatus, "processing");
    updateStatus(textStatus, "processing");
    updateStatus(navigationStatus, "processing");

    const formData = new FormData();

    formData.append(
        "image",
        imageInput.files[0]
    );

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

        console.log("STEP 1");
        console.log(result);

        updateStatus(visionStatus, "completed");
        console.log("STEP 2");

        updateStatus(textStatus, "completed");
        console.log("STEP 3");

        updateStatus(navigationStatus, "completed");
        console.log("STEP 4");

        ocrOutput.textContent =
            result.ocr_text || "No OCR text";
        console.log("STEP 5");

        translatedOutput.textContent =
            result.transliterated_text || "No transliteration";
        console.log("STEP 6");

        // -------------------------------
        // Pretty Navigation Output
        // -------------------------------

        navigationOutput.innerHTML = "";

        if (
            result.navigation &&
            result.navigation.navigation_items
        ) {

            result.navigation.navigation_items.forEach(item => {

                navigationOutput.innerHTML += `

                    <p><strong>Category:</strong> ${item.category}</p>

                    <p><strong>Text:</strong><br>
                    ${item.transliterated_text}</p>

                    <p><strong>Meaning:</strong><br>
                    ${item.interpretation}</p>

                    <hr>

                `;

            });

        } else {

            navigationOutput.textContent =
                "No navigation guidance";

        }

    }
    catch (error) {

        console.error(error);

        updateStatus(visionStatus, "error");
        updateStatus(textStatus, "error");
        updateStatus(navigationStatus, "error");

        ocrOutput.textContent = "";

        translatedOutput.textContent = "";

        navigationOutput.textContent =
            "❌ " + error.message;

    }
    finally {

        translateBtn.disabled = false;

        translateBtn.textContent = "🚀 Translate";

    }

});