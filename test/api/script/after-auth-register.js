try {
    const responseData = pm.response.json();
    
    if (responseData.code == 200 && responseData.data) {
        const { token, refreshToken, userId } = responseData.data;
        
        pm.collectionVariables.set("bearerToken", token);
        pm.collectionVariables.set("refreshToken", refreshToken);
        pm.collectionVariables.set("userId", userId);
    }
} catch (error) {
    console.error("Error processing register response:", error.message);
}