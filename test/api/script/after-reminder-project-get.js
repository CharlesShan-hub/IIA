try {
    const responseData = pm.response.json();
    
    if (responseData.code === 200 && responseData.data) {
        const projects = responseData.data;
        
        // 创建一个项目ID到项目对象的映射
        const projectMap = {};
        const projectNameMap = {};
        const projectList = [];
        
        projects.forEach(project => {
            // 保存到映射中，方便通过ID查找
            projectMap[project.projectId] = project;
            
            // 保存到名称映射中，方便通过名称查找
            projectNameMap[project.name] = project;
            
            // 保存到列表中，方便遍历
            projectList.push(project);
        });
        
        // 将数据保存到环境变量中
        // 注意：Postman环境变量只能存储字符串，所以我们需要序列化对象
        pm.collectionVariables.set("projectMap", JSON.stringify(projectMap));
        pm.collectionVariables.set("projectNameMap", JSON.stringify(projectNameMap));
        pm.collectionVariables.set("projectList", JSON.stringify(projectList));
        
        // 也可以保存一些统计信息
        pm.collectionVariables.set("projectCount", projects.length.toString());
        
        console.log(`Saved ${projects.length} projects to environment variables`);
        console.log("Available projects:", projects.map(p => `${p.projectId}: ${p.name}`).join(", "));
        
        // 设置第一个项目为当前选中的项目（如果有的话）
        if (projects.length > 0) {
            pm.collectionVariables.set("currentProjectId", projects[0].projectId.toString());
            pm.collectionVariables.set("currentProjectName", projects[0].name);
        }
    } else {
        console.warn("Failed to save projects: Invalid response or no data");
    }
} catch (error) {
    console.error("Error processing project get response:", error.message);
}