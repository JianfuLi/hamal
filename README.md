MySQL全文索引同步中间件

------

我们常常有全文搜索的需求，但MySQL数据库并不能很好的满足我们这个需求；因此我们常常需要另外部署solr/elasticsearch这样的服务来帮助我们进行全文搜索。使用这些全文索引的服务往往需要我在代码中自行控制数据的同步，增加代码量的同时也增加了复杂度。

hamal把自身伪装成MySQL的slave，解析master同步过来的binlog，自动推送到全文搜索服务中。

------

## 如何使用

首先，修改MySQL的binlog同步配置

### 修改my.cnf

```shell
[mysqld]
binlog-format = ROW
```
注意，binlog-format只能为ROW

### 修改setting.py 

```python
CONNECTION_SETTINGS = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "passwd": "123456"
}
SERVER_ID = 3
BLOCKING = True
RESUME_STREAM = True

PROVIDER = ElasticSearchProvider({'host': 'localhost', 'port': 9200})
PROJECTIONS = {
    'rpl_test': {
        'search': Mapper.search_converter
    }
}
```

### 运行程序

```shell
python hamal.py
```

