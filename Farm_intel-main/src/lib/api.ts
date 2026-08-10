export const getCropRecommendations = async (payload: any) => {
  try {
    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    return await res.json();
  } catch (err) {
    console.error("API Error:", err);
    return null;
  }
};