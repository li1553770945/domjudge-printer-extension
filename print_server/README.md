# 打印服务器

## 工作原理
开启一个http服务器，domjudge使用http添加请求，客户端通过轮询不断查询未打印的请求。

## 使用方法

1. `pip install -r requirements.txt`安装依赖。
2. 在domjudge的管理页面设置命令，注意把地址替换掉。
```shell
curl -X POST -H Content-Type:multipart/form-data
-F team_name=[teamname]
-F team_id=[teamid]
-F language=[language]
-F location=[location]
-F original_name=[original]
-F file=@[file]
http://192.168.1.194:8000/print/  2>&1
```
如果提示`SQLSTATE[22001]: String data, right truncated: 1406 Data too long for column extrainfo`,则执行以下sql语句修改长度：
```sql
USE domjudge;
ALTER TABLE auditlog MODIFY extra_info VARCHAR(511);
```

3. 使用`uwsgi -i uwsgi.ini`启动服务端。