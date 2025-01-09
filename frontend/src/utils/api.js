const BASE_URL = "https://your-backend-api-url.com";

export const analyzeText = async (text) => {
  try {
    const response = await fetch(`${BASE_URL}/classify`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch data");
    }

    return await response.json();
  } catch (error) {
    console.error("Error analyzing text:", error);
    return null;
  }
};
