const API_BASE_URL = window.location.origin;

export async function processImage(formData) {

    const response = await fetch(
        `${API_BASE_URL}/process-image`,
        {
            method: "POST",
            body: formData
        }
    );

    if (!response.ok) {

        let errorMessage = "Unknown error";

        try {

            const error = await response.json();

            errorMessage = error.detail || JSON.stringify(error);

        } catch {

            errorMessage = await response.text();

        }

        throw new Error(errorMessage);

    }

    return await response.json();

}