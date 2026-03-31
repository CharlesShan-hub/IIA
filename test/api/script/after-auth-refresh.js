try {
    const responseData = pm.response.json();
    
    if (responseData.code == 200 && responseData.data) {
        const { accessToken, refreshToken } = responseData.data;
        
        pm.collectionVariables.set("bearerToken", accessToken);
        pm.collectionVariables.set("refreshToken", refreshToken);
    }
} catch (error) {
    console.error("Error processing refresh response:", error.message);
}