# README

本节为api测试，首先从swagger导入api（第一个json）

```shell
https://localhost:8080/v3/api-docs
```

postman预先配置（第二个json）

```shell
test/api/env/iia-dev.postman_environment.json
```

最后要手动添加每一个前处理后处理脚本，运行generate脚本生成postman collection