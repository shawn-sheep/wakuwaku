# Milestone 1 Report - WAKUWAKU 插画分享站

## 项目背景

在当今数字时代，二次元文化已经成为了全球范围内广受欢迎的文化现象。二次元插画是一种独特而富有创意的艺术形式，它通过可爱、夸张和富有表现力的角色形象，吸引了大量的追随者和创作者。也诞生出众多供爱好者们交流、分享和欣赏二次元插画的平台。

这些插画平台如 Pixiv、Danbooru 等通常都具有完善的标签系统，可以帮助用户快速地找到自己感兴趣的图片，也可以帮助网站管理和分类图片。标签可以分为很多种类，比如作者、来源、角色等等。通过组合不同的标签，用户可以实现精确和灵活的搜索功能。

最近一年，本来只是为了方便用户搜索的标签系统又在大模型领域发挥了更大的作用，各种 Text to Image 模型的出现，让用户可以通过输入自然语言，生成自己想要的图片。而网站的标签系统，天然就是一个庞大的训练数据集。如基于 Stable Diffusion 的应用最广泛的微调模型 NovelAI，其训练数据就来自插画网站 Danbooru 的标签系统。

本项目旨在设计一个方便广大二次元爱好者交流、分享和欣赏二次元插画的平台，支持用户上传自己的作品，为作品打分，标注各种详细的标签，并通过组合不同的标签和筛选条件完成个性化的插画搜索。我们参考了一些已有的二次元插画图片站，比如 Pixiv、Danbooru 等，学习了它们的设计思路和技术实现，并结合我们自己的想法和需求，设计了这个项目。

## 数据集的基本情况

Danbooru 提供了官方的 API 接口：https://danbooru.donmai.us/wiki_pages/help:api
该站插画总量约为 600 万张，标签总量约为 200 万个。我们计划使用 Danbooru 的 API 接口，爬取其中的 10 万张图片及其相关数据，作为我们的数据集。

由于关系型数据库不适合存储大量二进制数据，一般数据库中只存储图片的 URL，并使用专门的存储解决方案（如对象存储）来处理大型的图片文件。我们目前直接使用 Danbooru 的图床，数据库中只存储图片的元数据，包括图片的标签、作者、来源、评分、图床 URL 等等。

### Sample Database

## 应用的基本功能

### 用户注册与登录

用户可以通过注册账号的方式，创建自己的账号。注册时需要提供用户名、密码和邮箱。注册成功后，用户可以通过用户名或邮箱和密码登录。

### 图片上传与管理

用户可以上传自己的图片，上传时需要提供图片的标题、来源、标签、评分和图片文件。其中标签可以从已有的标签中选择，也可以自己输入新的标签。评分可以是 SFW（适合所有人）或者 NSFW（不适合所有人）。图片文件可以是 PNG、JPG 或 GIF 格式。

用户可以管理自己上传的图片，包括修改图片的标题、来源、标签、评分和图片文件，也可以删除自己上传的图片。

### 标签和分类

用户可以为图片打上标签，标签可以分为很多种类，比如作者、来源、角色等等。同时，建立分类系统，让用户可以将插画作品归类到不同的主题或类别下。

### 搜索与浏览

用户可以根据标签、关键词或分类查找感兴趣的插画作品。同时，提供浏览功能，让用户可以按照不同的排序方式（如热门、最新）来发现和浏览作品。

标签分为 5 种：
```sql
0: General 通用标签
1: Artist 作者
3: Copyrights 所属作品
4: Characters 角色
5: Meta 元标签
```

用户也可以按照插画的用户得分来筛选作品，例如筛选出大于某个分数的作品。

### 评论与打分

用户可以对插画作品进行评论，也可以对插画作品进行打分（-1 或 +1）。

## 数据库设计

### E/R diagram

![](2023-05-15-21-54-43.png)

### Tables

```c
post(post_id, account_id, title, source, score, content, created_at)
PK: post_id
FK: account_id -> account(account_id)

image(image_id, post_id, name, preview_url, sample_url, original_url)
PK: image_id
FK: post_id -> post(post_id)

tag(tag_id, type, name, count)
PK: tag_id

post_tag(post_id, tag_id)
PK: (post_id, tag_id)
FK: post_id -> post(post_id)
FK: tag_id -> tag(tag_id)

account(account_id, username, password, email, created_at)
PK: account_id

comment(comment_id, post_id, account_id, content, created_at)
PK: comment_id
FK: post_id -> post(post_id)
FK: account_id -> account(account_id)

vote(post_id, account_id, value)
PK: (post_id, account_id)
FK: post_id -> post(post_id)
FK: account_id -> account(account_id)
```

### 功能以及对应的SQL语句

#### 用户注册

在用户注册时，需要插入新的账户记录：

```sql
INSERT INTO account (username, password, email, created_at)
VALUES (?, ?, ?, NOW());
```

#### 用户登录

在用户登录时，需要查询账户记录，判断用户名和密码是否匹配：

```sql
SELECT * FROM account 
WHERE (username = ? OR email = ?) AND password = ?;
```

#### 图片上传

在用户上传图片时，你\需要先插入一个新的 post 记录，然后再插一个新的 image 记录：

```sql
INSERT INTO post (account_id, title, source, score, content, created_at)
VALUES (?, ?, ?, ?, ?, NOW());

INSERT INTO image (post_id, name, preview_url, sample_url, original_url)
VALUES (?, ?, ?, ?, ?);
```

#### 图片管理

用户可以修改他们上传的图片的信息：

```sql
UPDATE post 
SET title = ?, source = ?, score = ?, content = ? 
WHERE post_id = ? AND account_id = ?;

UPDATE image 
SET name = ?, preview_url = ?, sample_url = ?, original_url = ? 
WHERE image_id = ?;
```

用户也可以删除他们上传的图片：

```sql
DELETE FROM post 
WHERE post_id = ? AND account_id = ?;
```

#### 标签和分类

用户可以给他们的图片添加标签：

```sql
INSERT INTO post_tag (post_id, tag_id)
VALUES (?, ?);
```

#### 搜索与浏览

用户可以根据标签、关键词或分类搜索图片：

```sql
SELECT * FROM post 
JOIN post_tag ON post.post_id = post_tag.post_id
JOIN tag ON post_tag.tag_id = tag.tag_id
WHERE tag.name LIKE ?;

SELECT * FROM post 
WHERE title LIKE ? OR content LIKE ?;
```
用户也可以按照不同的排序方式浏览图片，例如按照创建时间或得分：

```sql
SELECT * FROM post 
ORDER BY created_at DESC;

SELECT * FROM post 
ORDER BY score DESC;
```

#### 评论与打分

用户可以对图片进行评论：

```sql
INSERT INTO comment (post_id, account_id, content, created_at)
VALUES (?, ?, ?, NOW());
```

用户也可以对图片进行打分：

```sql
INSERT INTO vote (post_id, account_id, value)
VALUES (?, ?, ?);
```