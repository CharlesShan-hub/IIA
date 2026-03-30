# IIA - Intelligent Information Assistant
![IIA Demo](./assets/pic/IMG_1174.jpg)

## Introduction

下线运行的容器
```shell
docker compose down -v
```

下线并且删掉容器、网络、命名卷
```shell
docker compose down -v --remove-orphans
```

运行docker compose
```shell
docker compose up -d
```

进入mysql容器
```shell
docker exec -it iia-mysql mysql -u root -p
```

进入redis容器
```shell
docker exec -it iia-redis redis-cli
```

然后进去输入认证内容
```shell
auth default 123456 # 默认用户
auth iia-app 123456 # 登录用户
```

---

## Progress

- [x] 认证模块后端
- [ ] 备忘录模块后端
  - [x] Project
  - [x] Task
  - [ ] Recurrence
  - [ ] History
  - [x] Tag
  - [x] TaskTag

完成了从task到recurrence的转换
还需要完成循环任务子任务的管理

---

在apifox里边，从swagger导入api
```shell
https://localhost:8080/v3/api-docs
```

然后在login接口添加后置处理

```javascript
// 提取响应中的token并保存
try {
    const responseData = pm.response.json();
    
    // 检查响应结构
    if (!responseData) {
        throw new Error("Response is empty");
    }
    
    // 使用 == 而不是 ===，更宽松的类型检查
    if (responseData.code == 200 && responseData.data) {
        const { token, refreshToken, userId } = responseData.data;
        
        if (!token || !refreshToken || !userId) {
            throw new Error("Missing token fields in response data");
        }
        
        // 直接保存到bearerToken（Apifox默认变量名）
        pm.environment.set("bearerToken", token);
        pm.environment.set("refresh_token", refreshToken);
        pm.environment.set("user_id", userId);
        
        // 可选：同时保存到集合变量
        pm.collectionVariables.set("bearerToken", token);
        pm.collectionVariables.set("refresh_token", refreshToken);
        pm.collectionVariables.set("user_id", userId);
        
        console.log("✅ Login successful, tokens saved");
        console.log(`User ID: ${userId}`);
        console.log(`bearerToken: ${token.substring(0, 30)}...`);
        
    } else {
        console.error("❌ Login failed");
        console.error("Code:", responseData.code);
        console.error("Message:", responseData.msg);
    }
    
} catch (error) {
    console.error("❌ Error processing login response:", error.message);
    console.error("Response text:", pm.response.text());
}
```
