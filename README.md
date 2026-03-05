# IIA - Intelligent Information Assistant
![IIA Demo](./assets/pic/IMG_1174.jpg)

## Introduction

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