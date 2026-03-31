try {
    const responseData = pm.response.json();
    
    if (responseData.code == 200 && responseData.data) {
        const { username, userId } = responseData.data;
        
        pm.collectionVariables.set("userId", userId);
        pm.collectionVariables.set("username", username);
    }
} catch (error) {
    console.error("Error processing profile response:", error.message);
}