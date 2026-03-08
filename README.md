# IIA - Intelligent Information Assistant
![IIA Demo](./assets/pic/IMG_1174.jpg)

## Introduction

下线运行的容器
```shell
docker compose down -v
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



---

## Progress

- [x] 认证模块后端
- [ ] 备忘录模块后端
  - [x] Project
  - [ ] Task
  - [ ] Recurrence
  - [ ] History
  - [ ] Tag
  - [ ] TaskTag
