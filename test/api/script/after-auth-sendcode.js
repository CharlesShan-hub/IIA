try {
    const responseData = pm.response.json();
    
    if (responseData.code == 200 && responseData.data) {
        const { token, refreshToken, userId } = responseData.data;
        
        pm.environment.set("code", code);
    }
} catch (error) {
    console.error("Error processing sendcode response:", error.message);
}