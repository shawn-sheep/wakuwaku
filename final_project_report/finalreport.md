# Final Project Report - WAKUWAKU 插画分享站

## 项目背景

在当今数字时代，二次元文化已经成为了全球范围内广受欢迎的文化现象。二次元插画是一种独特而富有创意的艺术形式，它通过可爱、夸张和富有表现力的角色形象，吸引了大量的追随者和创作者。也诞生出众多供爱好者们交流、分享和欣赏二次元插画的平台。

这些插画平台如 Pixiv、Danbooru 等通常都具有完善的标签系统，可以帮助用户快速地找到自己感兴趣的图片，也可以帮助网站管理和分类图片。标签可以分为很多种类，比如作者、来源、角色等等。通过组合不同的标签，用户可以实现精确和灵活的搜索功能。

最近一年，本来只是为了方便用户搜索的标签系统又在大模型领域发挥了更大的作用，各种 Text to Image 模型的出现，让用户可以通过输入自然语言，生成自己想要的图片。而网站的标签系统，天然就是一个庞大的训练数据集。如基于 Stable Diffusion 的应用最广泛的微调模型 NovelAI，其训练数据就来自插画网站 Danbooru 的标签系统。

本项目旨在设计一个方便广大二次元爱好者交流、分享和欣赏二次元插画的平台，支持用户上传自己的作品，为作品打分，标注各种详细的标签，并通过组合不同的标签和筛选条件完成个性化的插画搜索。我们参考了一些已有的二次元插画图片站，比如 Pixiv、Danbooru 等，学习了它们的设计思路和技术实现，并结合我们自己的想法和需求，设计了这个项目。

## 数据集的基本情况

Danbooru 提供了官方的 API 接口：https://danbooru.donmai.us/wiki_pages/help:api
该站插画总量约为 600 万张，标签总量约为 200 万个。我们计划使用 Danbooru 的 API 接口，爬取其中的 100 万张图片及其相关数据，作为我们的数据集。

由于关系型数据库不适合存储大量二进制数据，一般数据库中只存储图片的 URL，并使用专门的存储解决方案（如对象存储）来处理大型的图片文件。我们目前直接使用 Danbooru 的图床，数据库中只存储图片的元数据，包括图片的标签、作者、来源、评分、图床 URL 等等。

## 数据建模的假设

每个用户都有自己的账户(account)，用户可以发布(upload)帖子(post)，一个帖子会包含多个图片(image)，用户可以给帖子投票(votes)喜欢还是不喜欢，用户可以收藏(favorite)帖子，每一个帖子都有多个标签(tag)。用户可以评论(comment)帖子，还可以对评论进行回复(reply_to)。

## ER设计图

![ERdiagram](db%E6%94%B9_01.jpg)

## 数据库表结构

```sql
-- postgreSQL
CREATE TABLE account (
    account_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE post (
    post_id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    source VARCHAR(255),
    score INTEGER NOT NULL,
    fav_count INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    rating CHAR(1) NOT NULL DEFAULT 's',
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);

CREATE TABLE image (
    image_id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    preview_url VARCHAR(255) NOT NULL,
    sample_url VARCHAR(255) NOT NULL,
    original_url VARCHAR(255) NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE
);

CREATE TABLE tag (
    tag_id SERIAL PRIMARY KEY,
    type INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    count INTEGER NOT NULL
);

CREATE TABLE post_tag (
    post_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag(tag_id) ON DELETE CASCADE
);

CREATE TABLE comment (
    comment_id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL,
    parent_id INTEGER,
    account_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES comment(comment_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);

CREATE TABLE vote (
    post_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    value INTEGER NOT NULL,
    PRIMARY KEY (post_id, account_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);

CREATE TABLE favorite (
    post_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, account_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES account(account_id)
);
```

## 用户界面介绍

### 界面描述：

#### 欢迎页，注册页，登录页：

在访问欢迎页前会检查用户的cookie以判断用户是否处于在线状态，如果属于则会自动跳转到主页。在欢迎页，用户可以选择注册或者登录。用户可以使用邮箱注册一个账号并且使用用户名进行登录，登录成功后会跳转到首页。

#### 首页：

用户在访问首页前也会检查用户的登录状态如果登录失效则会跳回到欢迎页。在首页用户可以看到最新更新的图片和图片排行榜，同时还有一个可以无限下拉的图片展示框展示图片推荐。用户点击缩略图后会显示一级详情页，在这里用户可以看到图片的部分信息并进行点赞收藏操作。再次点击图片会进入二级图片详情页。
#### 二级图片详情页：

在这个页面中，用户可以看到图片详细信息和图片的评论。用户可以对图片进行评论也可以对评论进行回复。点击标签可以直接跳转到对应标签的搜索页。点击上传者可以看到上传者首页。

#### 搜索页：

用户可以对标签，全文内容进行搜索，在搜索标签是有自动匹配功能，可以同时搜索多个标签。可以对搜索结果基于时间和热度进行排序，同样可以选择想要展示的分级。图片的展示框依然是可以无限下拉的。

#### 标签页：

可以看到不同种类的热门标签。

#### 用户页：

在用户页中可以看到对应用户的上传和收藏。

#### 上传页：

点击用户页中的上传按钮或者工具栏的上传图片选项就可以进入上传页。在上传页中用户可以上传图片。

#### 信息修改页：

点击用户页中的修改按钮或者工具栏的信息修改选项就可以进入信息修改页。在信息修改页中用户可以更改自己的用户名，邮箱和头像。

#### 工具栏：
点击用户头像就可以唤出工具栏，用户可以在工具栏中进入个人信息页，上传页和信息修改页。同样也可以登出自己的账号。


## 平台选择

我们选择的平台是Flask和Vue.js，Flask是一个基于Python的轻量级Web应用框架，Vue.js是一个构建数据驱动的web界面的渐进式框架，我们将使用Flask作为后端框架，Vue.js作为前端框架，实现一个基于Web的二次元插画分享站。

## 数据库性能调教

### Posts 查询

查询符合条件的是本站的核心功能，应该可以在各种排序顺序、筛选条件下快速查询到结果。

#### 1. 根据标签查询

第一个核心条件是标签，用户可以通过标签来筛选帖子。

##### 1.1 单标签查询
   
考虑在只有主键索引 `post_tag_pkey(post_id, tag_id)` 的情况下，查询某个标签下最近发布的100条帖子。（post_id 与发布时间成正相关）

```sql
BEGIN;
DROP INDEX tag_post_index;
DROP INDEX tag_index;

EXPLAIN ANALYSE
SELECT post_id FROM post_tag WHERE tag_id = 1442931 -- tag: 1442931	4	amiya_(arknights)	5150
ORDER BY post_id DESC
LIMIT 100;

ROLLBACK;
```

```sql
Limit  (cost=0.56..22632.54 rows=100 width=4) (actual time=1.297..91.127 rows=100 loops=1)
  ->  Index Only Scan Backward using post_tag_pkey on post_tag  (cost=0.56..458750.60 rows=2027 width=4) (actual time=1.296..91.103 rows=100 loops=1)
        Index Cond: (tag_id = 1442931)
        Heap Fetches: 100
Planning Time: 0.205 ms
Execution Time: 91.168 ms
```

可以看到在只有主键索引的情况下，查询计划为 `Index Only Scan Backward using post_tag_pkey on post_tag`，也就是从高到低遍历所有的 `post_tag`，然后再根据 `tag_id` 筛选出符合条件的结果，这个查询计划的时间复杂度为 `O(n)`，查询时间随着数据量（以及`OFFSET`）的增加而增加。

此时我们可以考虑为 `tag_id` 建立索引，这样就可以直接根据 `tag_id` 筛选出符合条件的结果。

```sql
CREATE INDEX tag_index ON public.post_tag USING btree (tag_id)
```

```sql
Limit  (cost=2336.44..2336.69 rows=100 width=4) (actual time=4.264..4.275 rows=100 loops=1)
  ->  Sort  (cost=2336.44..2341.51 rows=2027 width=4) (actual time=4.263..4.267 rows=100 loops=1)
        Sort Key: post_id DESC
        Sort Method: top-N heapsort  Memory: 34kB
        ->  Index Scan using tag_index on post_tag  (cost=0.56..2258.97 rows=2027 width=4) (actual time=1.436..3.833 rows=2162 loops=1)
              Index Cond: (tag_id = 1442931)
Planning Time: 0.918 ms
Execution Time: 4.327 ms
```

可以看到查询计划为 `Index Scan using tag_index on post_tag`，也就是根据 `tag_id` 筛选出符合条件的结果，然后再根据 `post_id` 降序排序，最后取前100条结果。

这个用时已经改进了很多，不过 `Sort` 还是一个阻塞算子，也就是需要先找到所有符合条件的结果，然后再进行排序，这个查询计划的时间复杂度为 `O(nlogn)`，其中 `n` 为符合条件的结果数量，测试语句中的 `tag` 只有 `5150` 条记录，所以用时较短，若是 `tag` 的数量更多，用时会更长。

此时考虑建立联合索引 `tag_post_index(tag_id, post_id)`，这样就可以直接根据 `tag_id` 筛选出符合条件的结果，并且已经按照 `post_id` 降序排序，不需要再进行排序。

```sql
CREATE UNIQUE INDEX tag_post_index ON public.post_tag USING btree (tag_id, post_id)
```

```sql
Limit  (cost=0.56..112.03 rows=100 width=4) (actual time=0.027..0.087 rows=100 loops=1)
  ->  Index Only Scan Backward using tag_post_index on post_tag  (cost=0.56..2260.01 rows=2027 width=4) (actual time=0.026..0.078 rows=100 loops=1)
        Index Cond: (tag_id = 1442931)
        Heap Fetches: 100
Planning Time: 0.222 ms
Execution Time: 0.119 ms
```

可见执行时间只需要 `0.119 ms`，不过当 `OFFSET` 较大时，用时会变长，因为需要先遍历 `OFFSET` 个结果，因此在实际操作中，我们可以让前端记录上次查询的最后一个 `post_id`，然后在下次查询时，直接从这个 `post_id` 直接开始遍历。

##### 1.2 多标签查询

