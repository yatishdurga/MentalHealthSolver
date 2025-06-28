const API_BASE_URL = "http://127.0.0.1:8000"; // OR use http://localhost:8000 if needed

export const analyzeText = async (text) => {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error("Failed to analyze text");
    }

    return await response.json();
  } catch (error) {
    console.error("API error:", error.message);
    throw error;
  }
};
