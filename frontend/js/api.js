const API_URL = obtenerApiUrl();

function obtenerApiUrl() {
    const configurada = localStorage.getItem("parksmart_api_url");
    if (configurada) return configurada.replace(/\/$/, "");

    const hostname = window.location.hostname || "127.0.0.1";
    const protocolo = window.location.protocol === "https:" ? "https:" : "http:";
    return `${protocolo}//${hostname}:8000`;
}

async function apiRequest(endpoint, opciones = {}) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 7000);

    try {
        const respuesta = await fetch(`${API_URL}${endpoint}`, {
            ...opciones,
            headers: {
                "Content-Type": "application/json",
                ...(typeof obtenerTokenAcceso === "function" && obtenerTokenAcceso() && localStorage.getItem("parksmart_demo_session") !== "true"
                    ? { "Authorization": `Bearer ${obtenerTokenAcceso()}` }
                    : {}),
                ...(opciones.headers || {})
            },
            signal: controller.signal
        });

        const contentType = respuesta.headers.get("content-type") || "";
        const contenido = contentType.includes("application/json")
            ? await respuesta.json()
            : await respuesta.text();

        if (!respuesta.ok) {
            const detalle = contenido?.detail || contenido || `Error ${respuesta.status}`;
            throw new Error(typeof detalle === "string" ? detalle : JSON.stringify(detalle));
        }

        return contenido;
    } catch (error) {
        if (error.name === "AbortError") {
            throw new Error("La API tardó demasiado en responder.");
        }
        throw error;
    } finally {
        clearTimeout(timeout);
    }
}

function apiGet(endpoint) {
    return apiRequest(endpoint);
}

function apiPost(endpoint, datos) {
    return apiRequest(endpoint, {
        method: "POST",
        body: JSON.stringify(datos)
    });
}

function apiPut(endpoint, datos = null) {
    return apiRequest(endpoint, {
        method: "PUT",
        body: datos ? JSON.stringify(datos) : undefined
    });
}

function apiDelete(endpoint) {
    return apiRequest(endpoint, { method: "DELETE" });
}

async function verificarApi() {
    await apiGet("/espacios/disponibles");
    return true;
}
