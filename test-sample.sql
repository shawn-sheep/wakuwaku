-- 选择 post 表和 image 表的字段
SELECT
    post.post_id AS post_post_id,
    post.account_id AS post_account_id,
    post.title AS post_title,
    post.source AS post_source,
    post.score AS post_score,
    post.fav_count AS post_fav_count,
    post.content AS post_content,
    post.created_at AS post_created_at,
    post.rating AS post_rating,
    image.preview_url AS image_preview_url,
    image.width AS image_width,
    image.height AS image_height,
    anon_1.image_count AS anon_1_image_count -- 计算字段，表示每个 post 关联的 image 数量
FROM
    post -- 主表是 post
    JOIN (
        SELECT
            image.post_id AS post_id,
            min(image.image_id) AS min_image_id,
            -- 每个 post 关联的最小 image_id
            count(image.image_id) AS image_count -- 每个 post 关联的 image 数量
        FROM
            image
        WHERE
            image.post_id IN (
                SELECT
                    anon_2.post_id
                FROM
                    (
                        -- 选择具有指定标签和评级的 post
                        SELECT
                            post.post_id AS post_id
                        FROM
                            post
                        WHERE
                            (
                                EXISTS (
                                    SELECT
                                        1
                                    FROM
                                        post_tag
                                    WHERE
                                        post.post_id = post_tag.post_id
                                        AND post_tag.tag_id = %(tag_id_1) s
                                )
                            )
                            AND post.rating IN (%(rating_1_1) s)
                        ORDER BY
                            post.post_id DESC
                        LIMIT
                            %(param_1) s OFFSET %(param_2) s -- 对结果进行分页
                    ) AS anon_2
            )
        GROUP BY
            image.post_id
    ) AS anon_1 ON post.post_id = anon_1.post_id
    JOIN image ON image.image_id = anon_1.min_image_id -- 连接 image 表，条件是 image_id 等于最小的 image_id
ORDER BY
    post.post_id DESC;

-- 按 post_id 降序排序