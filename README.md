# WakuWaku

WakuWaku 插画分享站

## 主要功能

- 浏览插画
- 标签搜索
- 结果排序
- 上传插画
- 点赞收藏~~投币~~

## 快速部署

### Vue 前端

先进入前端目录
```bash
cd ./vue
```

Setup
```bash
npm install
```

开发环境编译 & 热重载
```bash
npm run serve
```

编译 & 打包
```bash
npm run build
```

### Flask 后端

安装依赖
```bash
pip install -r requirements.txt
```

启动后端开发环境
```bash
python run.py
```

### PostgreSQL 数据库

安装 `zhparser` 扩展，使用 `schema.sql` 在 PostgreSQL 中创建数据表

在 `run.py` 修改数据库 `URI`
```python
app.config["SQLALCHEMY_DATABASE_URI"] = "your database uri"
```

### 数据爬取

一个简陋的 Danbooru 爬虫在 `spider/spider.py`
你可以编写其他网站的爬虫，或添加自己的数据集