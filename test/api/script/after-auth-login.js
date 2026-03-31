try {
    const responseData = pm.response.json();
    
    if (responseData.code == 200 && responseData.data) {
        const { token, refreshToken, userId } = responseData.data;
        
        pm.environment.set("bearerToken", token);
        pm.environment.set("refreshToken", refreshToken);
        pm.environment.set("userId", userId);
    }
} catch (error) {
    console.error("Error processing login response:", error.message);
}