# Final Project Report - WAKUWAKU 插画分享站

## 项目背景

在当今数字时代，二次元文化已经成为了全球范围内广受欢迎的文化现象。二次元插画是一种独特而富有创意的艺术形式，它通过可爱、夸张和富有表现力的角色形象，吸引了大量的追随者和创作者。也诞生出众多供爱好者们交流、分享和欣赏二次元插画的平台。

这些插画平台如 Pixiv、Danbooru 等通常都具有完善的标签系统，可以帮助用户快速地找到自己感兴趣的图片，也可以帮助网站管理和分类图片。标签可以分为很多种类，比如作者、来源、角色等等。通过组合不同的标签，用户可以实现精确和灵活的搜索功能。

最近一年，本来只是为了方便用户搜索的标签系统又在大模型领域发挥了更大的作用，各种 Text to Image 模型的出现，让用户可以通过输入自然语言，生成自己想要的图片。而网站的标签系统，天然就是一个庞大的训练数据集。如基于 Stable Diffusion 的应用最广泛的微调模型 NovelAI，其训练数据就来自插画网站 Danbooru 的标签系统。

本项目旨在设计一个方便广大二次元爱好者交流、分享和欣赏二次元插画的平台，支持用户上传自己的作品，为作品打分，标注各种详细的标签，并通过组合不同的标签和筛选条件完成个性化的插画搜索。我们参考了一些已有的二次元插画图片站，比如 Pixiv、Danbooru 等，学习了它们的设计思路和技术实现，并结合我们自己的想法和需求，设计了这个项目。

## 数据集的基本情况

Danbooru 提供了官方的 API 接口：https://danbooru.donmai.us/wiki_pages/help:api
该站插画总量约为 600 万张，标签总量约为 200 万个。我们计划使用 Danbooru 的 API 接口，爬取其中的 10 万张图片及其相关数据，作为我们的数据集。

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

## 数据库性能调教

