try {
    const responseData = pm.response.json();
    
    if (responseData.code === 200 && responseData.data) {
        const newProject = responseData.data;
        
        console.log(`New project created: ${newProject.name} (ID: ${newProject.projectId})`);
        
        // 获取现有的项目数据
        const projectMapStr = pm.environment.get("projectMap");
        const projectNameMapStr = pm.environment.get("projectNameMap");
        const projectListStr = pm.environment.get("projectList");
        
        let projectMap = {};
        let projectNameMap = {};
        let projectList = [];
        
        // 如果已有项目数据，解析它
        if (projectMapStr && projectNameMapStr && projectListStr) {
            try {
                projectMap = JSON.parse(projectMapStr);
                projectNameMap = JSON.parse(projectNameMapStr);
                projectList = JSON.parse(projectListStr);
            } catch (error) {
                console.warn("Error parsing existing project data, starting fresh:", error.message);
            }
        }
        
        // 检查是否已存在相同ID的项目
        if (projectMap[newProject.projectId]) {
            console.warn(`Project with ID ${newProject.projectId} already exists. Updating...`);
            
            // 更新现有项目
            const oldProject = projectMap[newProject.projectId];
            
            // 如果名称改变了，需要更新名称映射
            if (oldProject.name !== newProject.name) {
                delete projectNameMap[oldProject.name];
                projectNameMap[newProject.name] = newProject;
            }
            
            // 更新项目列表中的项目
            const index = projectList.findIndex(p => p.projectId === newProject.projectId);
            if (index !== -1) {
                projectList[index] = newProject;
            }
        } else {
            // 添加新项目
            projectMap[newProject.projectId] = newProject;
            projectNameMap[newProject.name] = newProject;
            projectList.push(newProject);
            
            console.log(`Added new project to collection. Total projects: ${projectList.length}`);
        }
        
        // 更新项目映射
        projectMap[newProject.projectId] = newProject;
        
        // 保存更新后的数据到环境变量
        pm.collectionVariables.set("projectMap", JSON.stringify(projectMap));
        pm.collectionVariables.set("projectNameMap", JSON.stringify(projectNameMap));
        pm.collectionVariables.set("projectList", JSON.stringify(projectList));
        pm.collectionVariables.set("projectCount", projectList.length.toString());
        
        // 自动设置为当前项目
        pm.collectionVariables.set("currentProjectId", newProject.projectId.toString());
        pm.collectionVariables.set("currentProjectName", newProject.name);
        
        console.log(`Set current project to: ${newProject.name} (ID: ${newProject.projectId})`);
        
        // 打印更新后的项目列表
        console.log("Updated project list:", projectList.map(p => `${p.projectId}: ${p.name}`).join(", "));
    } else {
        console.warn("Failed to save new project: Invalid response or no data");
    }
} catch (error) {
    console.error("Error processing project create response:", error.message);
}