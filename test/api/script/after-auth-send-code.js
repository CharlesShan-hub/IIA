try {
    const responseData = pm.response.json();
    
    if (responseData.code == 200 && responseData.data) {
        const { code } = responseData.data;
        
        pm.collectionVariables.set("code", code);
    }
} catch (error) {
    console.error("Error processing sendcode response:", error.message);
}