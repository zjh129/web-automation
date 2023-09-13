# web-automation

> **免责声明：**

>本仓库的所有内容仅供学习和参考之用，禁止用于商业用途。任何人或组织不得将本仓库的内容用于非法用途或侵犯他人合法权益。本仓库所涉及的爬虫技术仅用于学习和研究，不得用于对其他平台进行大规模爬虫或其他非法行为。对于因使用本仓库内容而引起的任何法律责任，本仓库不承担任何责任。使用本仓库的内容即表示您同意本免责声明的所有条款和条件。

# 仓库描述



原理：利用[playwright](https://playwright.dev/)搭桥，保留登录成功后的上下文浏览器环境，通过执行JS表达式获取一些加密参数
通过使用此方式，免去了复现核心加密JS代码，逆向难度大大降低。

## 使用方法

1. 安装依赖库

```shell
pip install -r requirements.txt
```

2. 安装playwright浏览器驱动

```shell
playwright install
```

3、docker启用redis服务
```shell
docker run -itd --name local-redis -p 6379:6379 redis redis-server --appendonly yes
```

4、具体使用查看tests目录页下的测试用例