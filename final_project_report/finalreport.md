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
SELECT post_id FROM post_tag WHERE tag_id = 1442931 -- tag: 1442931	4	amiya_(arknights)	2162
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

当需要对多个tag的结果取交集时，就不能直接使用 `WHERE post_id = xxx` 来进行筛选了，最直觉的写法是直接使用 `INTERSECT`，以搜索 `amiya_(arknights)` 和 `1girl` 为例：

```sql
EXPLAIN ANALYSE
(SELECT post_id FROM post_tag WHERE tag_id = 1442931) -- tag: 1442931	4	amiya_(arknights)	2162
INTERSECT
(SELECT post_id FROM post_tag WHERE tag_id = 470575) -- tag: 470575	0	1girl	873907
ORDER BY post_id DESC
LIMIT 100;
```

```sql
Limit  (cost=246705.97..246706.22 rows=100 width=8) (actual time=307.838..307.850 rows=100 loops=1)
  ->  Sort  (cost=246705.97..246711.03 rows=2025 width=8) (actual time=307.837..307.843 rows=100 loops=1)
        Sort Key: "*SELECT* 1".post_id DESC
        Sort Method: top-N heapsort  Memory: 33kB
        ->  HashSetOp Intersect  (cost=0.56..246628.57 rows=2025 width=8) (actual time=307.500..307.705 rows=1287 loops=1)
              ->  Append  (cost=0.56..244447.52 rows=872421 width=8) (actual time=0.031..244.232 rows=876069 loops=1)
                    ->  Subquery Scan on "*SELECT* 1"  (cost=0.56..2279.24 rows=2027 width=8) (actual time=0.030..0.541 rows=2162 loops=1)
                          ->  Index Scan using tag_index on post_tag  (cost=0.56..2258.97 rows=2027 width=4) (actual time=0.029..0.368 rows=2162 loops=1)
                                Index Cond: (tag_id = 1442931)
                    ->  Subquery Scan on "*SELECT* 2"  (cost=0.56..237806.17 rows=870394 width=8) (actual time=0.030..195.276 rows=873907 loops=1)
                          ->  Index Scan using tag_index on post_tag post_tag_1  (cost=0.56..229102.23 rows=870394 width=4) (actual time=0.029..131.805 rows=873907 loops=1)
                                Index Cond: (tag_id = 470575)
Planning Time: 0.229 ms
Execution Time: 307.920 ms
```

然而，可以看到执行计划直接搜出两个子查询的结果，然后再进行 `HashSetOp Intersect`，这个算子的时间复杂度为 `O(n)`，其中 `n` 为两个子查询结果的数量之和，因此当两个子查询结果的数量之和较大时，用时会很长。
例子中 `amiya_(arknights)` 有 `2162` 条记录，`1girl` 有 `873907` 条记录，这种方法把满足 `1girl` 的所有记录都搜出来了，然后再进行交集运算，因此用时较长。

但如果使用下面的写法：

```sql
SELECT post_id
FROM post
WHERE
post_id IN (SELECT post_id FROM post_tag WHERE post_tag.tag_id = 1442931)
AND
post_id IN (SELECT post_id FROM post_tag WHERE post_tag.tag_id = 470575)
ORDER BY post_id DESC
LIMIT 100;
```

```sql
Limit  (cost=1.56..540.96 rows=100 width=4) (actual time=0.030..1.016 rows=100 loops=1)
  ->  Nested Loop  (cost=1.56..8917.82 rows=1653 width=4) (actual time=0.029..1.007 rows=100 loops=1)
        Join Filter: (post_tag.post_id = post.post_id)
        ->  Nested Loop  (cost=1.13..7875.50 rows=1660 width=8) (actual time=0.023..0.724 rows=100 loops=1)
              ->  Index Only Scan Backward using tag_post_index on post_tag  (cost=0.56..2260.01 rows=2027 width=4) (actual time=0.012..0.068 rows=215 loops=1)
                    Index Cond: (tag_id = 1442931)
                    Heap Fetches: 215
              ->  Index Only Scan using tag_post_index on post_tag post_tag_1  (cost=0.56..2.77 rows=1 width=4) (actual time=0.003..0.003 rows=0 loops=215)
                    Index Cond: ((tag_id = 470575) AND (post_id = post_tag.post_id))
                    Heap Fetches: 100
        ->  Index Only Scan using post_pkey on post  (cost=0.43..0.62 rows=1 width=4) (actual time=0.003..0.003 rows=1 loops=100)
              Index Cond: (post_id = post_tag_1.post_id)
              Heap Fetches: 38
Planning Time: 0.654 ms
Execution Time: 1.050 ms
```

可以看到，优化器把 `post_id IN subquery` 的操作转换成了 `Nested Loop` 算子，并从统计信息（由于默认的统计）中发现 `amiya_(arknights)` 的结果集较小，因此把 `amiya_(arknights)` 作为外层循环，把 `1girl` 作为内层循环，这样就可以避免把 `1girl` 的所有结果都搜出来了，而是在遍历 `amiya_(arknights)` 的结果时，每次都去 `1girl` 的结果集中查找，这样就可以把时间复杂度降低到 `O(n)`，其中 `n` 为 `amiya_(arknights)` 的结果集的大小。（有 `LIMIT` 限制时，时间取决于什么时候找到 `LIMIT` 条记录）

##### 1.3 按分数排序

分数代表用户 `vote.value` 的和，本站也支持按照分数来排序查询结果，但是 `post.score` 并不出现在 `post_tag` 表中，有一种方法是把 `score` 作为 `post_tag` 的一个属性，并添加`tag_score` 索引，但是这样会导致 `post_tag` 表的大小增加，而且 `score` 的更新会变得复杂。

另一种方法是建立联合索引 `score_post_id_index(score, post_id)`，其中 `post_id` 是为了在同分数时确定顺序。

```sql
CREATE UNIQUE INDEX score_post_id_index ON public.post USING btree (score, post_id)
```

接下来，利用或不利用这个索引，理论上有两种方法实现带 `LIMIT` 的按分数排序标签查询：

设 `P` 为结果集在数据集中占比，`N` 为 `post` 表的大小，`L` 为 `LIMIT` 的大小，我们假设结果在按分数排序的序列里均匀分布。

1. 使用 `score_post_id_index` 先不管其他条件，扫描 `score_post_id_index`，对每条记录检查是否满足其他条件，如果满足则加入结果集，一直到找到 `LIMIT` 条记录或者扫描完所有记录，每条记录满足条件的概率是 `P`，因此期望扫描的记录数为 `L / P`。如果 `P` 较大，那么这种方法效率较高。
   注意，前端可以存储当前的 `(score, post_id)`，那么在每次查询都可以从上次位置继续扫描，不需要考虑 `OFFSET`。

2. 直接先找出满足其他条件的记录，然后对这些记录按照分数排序，取前 `LIMIT` 条记录。这种方法的效率不受 `LIMIT` 的影响，固定需要找出 `P * N` 条记录，对其排序，取前 `LIMIT` 条记录。

当 `L / P < P * N` 也就是 `P > sqrt(L / N)` 时，第一种方法效率较高，否则第二种方法效率较高。
我们取 `L = 100`，`N = 1000000`，可以得到 `P > 0.01` 时第一种方法效率较高，也就是说，如果结果集在数据集中占比超过 `1%`，那么第一种方法效率较高。

接下来进行一些实验：
`night_sky` 有 `7391` 条记录，占比略小于 `1%`。

```sql
SELECT post_id
FROM post
WHERE
post_id IN (SELECT post_id FROM post_tag WHERE post_tag.tag_id = 166133)
ORDER BY score DESC, post_id DESC
LIMIT 100;
```

```sql
Limit  (cost=0.99..13103.50 rows=100 width=8) (actual time=0.186..43.331 rows=100 loops=1)
  ->  Nested Loop  (cost=0.99..1013217.56 rows=7733 width=8) (actual time=0.185..43.318 rows=100 loops=1)
        ->  Index Only Scan Backward using score_post_id_index on post  (cost=0.43..46667.72 rows=1066748 width=8) (actual time=0.014..13.387 rows=18840 loops=1)
              Heap Fetches: 17303
        ->  Index Only Scan using tag_post_index on post_tag  (cost=0.56..0.91 rows=1 width=4) (actual time=0.001..0.001 rows=0 loops=18840)
              Index Cond: ((tag_id = 166133) AND (post_id = post.post_id))
              Heap Fetches: 100
Planning Time: 0.373 ms
Execution Time: 43.383 ms
```

可以看到查询计划并没有按照我们计算的使用第二种方法，而是使用了第一种方法，用时 `43.383 ms`。

```sql
DROP INDEX score_post_id_index;
```

当我们禁用 `score_post_id_index` 时，查询计划如下：

```sql
Limit  (cost=24431.03..24431.28 rows=100 width=8) (actual time=25.644..25.656 rows=100 loops=1)
  ->  Sort  (cost=24431.03..24450.36 rows=7733 width=8) (actual time=25.643..25.649 rows=100 loops=1)
        Sort Key: post.score DESC, post.post_id DESC
        Sort Method: top-N heapsort  Memory: 32kB
        ->  Nested Loop  (cost=0.99..24135.48 rows=7733 width=8) (actual time=0.026..24.472 rows=7391 loops=1)
              ->  Index Only Scan Backward using tag_post_index on post_tag  (cost=0.56..8494.19 rows=7733 width=4) (actual time=0.018..2.145 rows=7391 loops=1)
                    Index Cond: (tag_id = 166133)
                    Heap Fetches: 7391
              ->  Index Scan using post_pkey on post  (cost=0.43..2.02 rows=1 width=8) (actual time=0.003..0.003 rows=1 loops=7391)
                    Index Cond: (post_id = post_tag.post_id)
Planning Time: 0.371 ms
Execution Time: 25.690 ms
```

可以看到查询计划使用了第二种方法，用时 `25.690 ms`，一定程度说明我们的分析是正确的，优化器在 `P` 接近 `1%` 时可能会选择更慢的方法。

当 `P` 更小时，如有 `4181` 条记录的 `light_purple_hair`，优化器就会正确选择第二种方法：

```sql
Planning Time: 0.368 ms
Execution Time: 13.909 ms
```

上述 `LIMIT` 设为 `100` 是为了更好体现两种方案的区别和界限，实际上本站的 `LIMIT` 在 `5` 左右，实际测试中执行时间一般小于 `10ms` 左右，可以接受。

#### 2. 统计信息

上述问题中，优化器要决定 `Nest Loop` 中谁是外循环，谁是内循环，要根据两个结果集的大小来决定，同时在按分数排序中，优化器需要知道 `P` 的大小，这些信息都是通过统计信息得到的。

然而默认的 `statistics_target` 为 `100`，这个数值决定了采样的记录数，以及记录的`most_common_vals，most_common_freqs，histogram_bounds` 信息的数量。

对于 `tag_id` 来说，`most_common_vals，most_common_freqs` 记录了前 `100` 个出现次数最多的 `tag_id`，也就是说，若采用默认设置，优化器只能知道前 `100` 个 `tag_id` 的出现次数，这对于我们的问题来说是不够的，我们需要有能力区分有 `5000` 个 `tag_id` 的记录和有 `500` 个 `tag_id` 的记录。（分数排序中，`P` 的大小）

```sql
ALTER TABLE post_tag ALTER COLUMN tag_id SET STATISTICS 10000;
ANAALYZE post_tag;
```

通过执行上述语句，我们可以将 `statistics_target` 设置为 `10000`（上限），得到更精确的统计信息，这样优化器就可以更好地选择执行计划。（实际上第一节的实验中，`statistics_target` 已经被设置为 `10000`）

#### 3. 全文检索

在 Post 表中，我们有 `title` 和 `content` 两个字段，我们希望用户可以通过关键词搜索到相关的 Post，这就需要用到全文检索。

```sql
CREATE TEXT SEARCH CONFIGURATION zhcfg (PARSER = zhparser);
ALTER TEXT SEARCH CONFIGURATION zhcfg ADD MAPPING FOR n,v,a,i,e,l WITH simple;
CREATE INDEX idx_fts_title_content ON post USING gin(to_tsvector('zhcfg', title || ' ' || content));
```

PostgreSQL 本身只有英文的全文检索，我们需要安装中文全文检索插件 `zhparser`，然后创建一个 `TEXT SEARCH CONFIGURATION`，并将其映射到 `zhparser`，最后创建一个 `GIN` 索引。

接下来简单对比一下和 `LIKE` 的性能区别

```sql
SELECT *
FROM post
WHERE title || ' ' || content LIKE '%胡桃%';
```

```sql
Seq Scan on post  (cost=0.00..55758.09 rows=341 width=212) (actual time=0.599..485.326 rows=2749 loops=1)
  Filter: ((((title)::text || ' '::text) || content) ~~ '%胡桃%'::text)
  Rows Removed by Filter: 1063999
Planning Time: 0.057 ms
Execution Time: 485.535 ms
```

```sql
SELECT *
FROM post
WHERE to_tsvector('zhcfg', title || ' ' || content) @@ to_tsquery('zhcfg', '胡桃');
```

```sql
Bitmap Heap Scan on post  (cost=26.17..3504.24 rows=2667 width=212) (actual time=0.925..4.007 rows=2741 loops=1)
  Recheck Cond: (to_tsvector('zhcfg'::regconfig, (((title)::text || ' '::text) || content)) @@ '''胡桃'''::tsquery)
  Heap Blocks: exact=2206
  ->  Bitmap Index Scan on idx_fts_title_content  (cost=0.00..25.50 rows=2667 width=0) (actual time=0.651..0.651 rows=2741 loops=1)
        Index Cond: (to_tsvector('zhcfg'::regconfig, (((title)::text || ' '::text) || content)) @@ '''胡桃'''::tsquery)
Planning Time: 0.170 ms
Execution Time: 4.172 ms
```

比 `LIKE` 快了 `100` 倍以上。