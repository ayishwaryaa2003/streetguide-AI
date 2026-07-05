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

        const body = await response.text();

        let errorMessage = body;

        try {
            const error = JSON.parse(body);
            errorMessage = error.detail || JSON.stringify(error);
        } catch {
            // body wasn't JSON
        }

        throw new Error(errorMessage);
    }

    return await response.json();

}