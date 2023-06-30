import requests
from tqdm import tqdm
import time

from model import Account, Post, Image, Tag, PostTag, Comment, Vote

proxies = {
    'http': 'http://localhost:7890',
    'https': 'http://localhost:7890'
}

headers = {
    'User-Agent': 'Mozilla/5.0'
}

base_url = 'https://danbooru.donmai.us'

username = 'yhzx233'
api_key = '9PP752CvjWZJMNKGdhFrposg'

def get_posts_json(limit, tags, last_id=None, direction='b'):
    '''获取 posts json 列表'''
    res = []

    with tqdm(total=limit, desc='Getting posts') as pbar:
        while len(res) < limit:
            url = f'{base_url}/posts.json?limit=200&tags={tags}'
            if last_id:
                url += f'&page={direction}{last_id}'

            while True:
                try:
                    response = requests.get(url, auth=(username, api_key), headers=headers, proxies=proxies)
                    if response.status_code == 200:
                        posts = response.json()
                        if not posts:
                            return res
                        res.extend(posts)
                        # last_id = posts[-1]['id']
                        last_id = direction == 'b' and posts[-1]['id'] or posts[0]['id']
                        break
                    else:
                        print(f'Error: {response.status_code}')
                        return res
                except Exception as e:
                    print(e)
                    time.sleep(1)

            pbar.update(len(posts))

    return res[:limit]

from urllib.parse import quote

def get_jsons(type: str, key : str, ids : list[int]) -> list:
    '''获取 type 类型的 json'''
    res = []

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    url = f'{base_url}/{type}.json'
    data = f'_method=get&limit=500&search[{key}]={quote(",".join(map(str, ids)), safe=",")}'

    while True:
        try:
            response = requests.post(url, data=data, auth=(username, api_key), headers=headers, proxies=proxies)

            if response.status_code == 200:
                res = response.json()
            else:
                print(f'Error: {response.status_code}')
                print(response.text)
            break
        except Exception as e:
            print(e)
            time.sleep(1)

    return res

import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
# url中@字符编码为%40
engine = sa.create_engine('postgresql://root:GaussdbPassword%40123@119.3.126.0:5432/postgres', pool_pre_ping=True)
Session = sessionmaker(bind=engine)

# 2023-05-09T07:07:14.411-04:00 转 2023-05-09 07:07:14
def convert_time(time : str):
    time = time.split('.')[0]
    time = time.split('T')
    time = time[0] + ' ' + time[1]
    return time

def process_accounts(account_ids):
    '''处理 accounts'''
    accounts = []
    # 每次处理 500 个
    for i in tqdm(range(0, len(account_ids), 500), desc='Getting accounts'):
        accounts.extend(get_jsons('users', 'id', account_ids[i:i+500]))

    with Session() as session:

        for account_json in tqdm(accounts, desc='Processing accounts'):
            account_id = account_json['id']

            # 如果 account 已存在，则跳过
            if session.query(Account).filter(Account.account_id == account_id).first():
                continue

            # 处理 account
            account = Account(
                account_id=account_id,
                username=account_json['name'],
                password='',
                email='',
                avatar_url='',
                created_at=convert_time(account_json['created_at']),
            )

            session.add(account)
        
        session.commit()

def process_posts(posts):
    '''处理 posts'''
    commentaries = []
    # 每次处理 500 个
    for i in tqdm(range(0, len(posts), 500), desc='Getting commentaries'):
        commentaries.extend(get_jsons('artist_commentaries', 'post_id', [post['id'] for post in posts[i:i+500]]))
    post_id_commentaries = {commentary['post_id']: commentary for commentary in commentaries}

    with Session() as session:

        existing_post_ids = session.query(Post.post_id).where(Post.post_id.between(min_post_id, max_post_id)).all()
        existing_post_ids = set([int(post_id) for post_id, in existing_post_ids])

        for post_json in tqdm(posts, desc='Processing posts / images'):
            post_id = post_json['id']

            post_title = post_id_commentaries.get(post_id, {}).get('original_title', '')
            post_description = post_id_commentaries.get(post_id, {}).get('original_description', '')

            # 如果 post 已存在，则UPDATE
            if post_id in existing_post_ids:
                session.execute(
                    text('UPDATE post SET title=:title, score=:score, content=:content, fav_count=:fav_count WHERE post_id=:post_id'),
                    {
                        'post_id': post_id,
                        'title': post_title[0:255],
                        'score': post_json['score'],
                        'content': post_description,
                        'fav_count': post_json['fav_count'],
                    }
                )
                continue

            # 处理 post
            post = Post(
                post_id=post_id,
                account_id=post_json['uploader_id'],
                title=post_title[0:255],
                source=post_json['source'][0:255],
                fav_count=post_json['fav_count'],
                score=post_json['score'],
                content=post_description,
                created_at=convert_time(post_json['created_at']),
                rating=post_json['rating'],
            )

            session.add(post)

            # 错误的 post
            if 'preview_file_url' not in post_json:
                continue

            # 处理 image
            image_json = post_json['media_asset']
            image = Image(
                image_id=image_json['id'],
                post_id=post_id,
                name='',
                preview_url=post_json['preview_file_url'],
                sample_url=post_json['large_file_url'],
                original_url=post_json['file_url'],
                width=image_json['image_width'],
                height=image_json['image_height'],
            )

            session.add(image)
        
        session.commit()

def process_tags(tag_names):
    '''处理 tags'''

    with Session() as session:

        existing_tags : list[Tag] = session.query(Tag).all()
        existing_tag_names = set(str(tag.name) for tag in existing_tags)
        tag_name_ids = {tag.name: tag.tag_id for tag in existing_tags}

        tag_names = list(set(tag_names) - set(existing_tag_names))

        print(f'Unknown tags: {len(tag_names)}')

        tags = []
        # 每次处理 500 个
        for i in tqdm(range(0, len(tag_names), 500), desc='Getting tags'):
            tags.extend(get_jsons('tags', 'name_normalize', tag_names[i:i+500]))
            tag_name_ids.update({tag['name']: tag['id'] for tag in tags})

        for tag_json in tqdm(tags, desc='Processing tags'):
            tag_id = tag_json['id']

            # 如果 tag 已存在，则跳过
            if tag_json['name'] in existing_tag_names:
                continue

            # 处理 tag
            tag = Tag(
                tag_id=tag_id,
                type=tag_json['category'],
                name=tag_json['name'],
                count=tag_json['post_count'],
            )

            session.add(tag)
        
        session.commit()
        
    return tag_name_ids

def process_post_tags(posts, tag_name_ids):
    '''处理 post_tags'''
    with Session() as session:
        # 筛选 post_id 在 max_post_id 到 min_post_id 之间
        existing_post_ids = session.query(PostTag.post_id).distinct().where(PostTag.post_id.between(min_post_id, max_post_id)).all()
        existing_post_ids = set(post_id for post_id, in existing_post_ids)

        for idx, post_json in tqdm(enumerate(posts), desc='Processing post_tags', total=len(posts)):
            post_tags = []
            post_id = post_json['id']

            if post_id in existing_post_ids:
                continue

            for tag_name in post_json['tag_string'].split(' '):

                post_tags.append(PostTag(
                    post_id=post_id,
                    tag_id=tag_name_ids[tag_name],
                ))

            session.add_all(post_tags)

            if idx % 1000 == 0:
                session.commit()

        session.commit()

if __name__ == '__main__':
    last_post_id = 5495919
    post_count = 10000
    with engine.connect() as conn:
        result = conn.execute('SELECT post_id FROM post WHERE rating = \'s\' ORDER BY post_id ASC LIMIT 1')
        last_post_id = result.fetchone()[0]
        print(f'Last post id: {last_post_id}')

    posts = get_posts_json(post_count, 'rating:g,s score:>10', last_post_id, direction='b')
    # post id 的极值
    max_post_id = posts[0]['id']
    min_post_id = posts[-1]['id']
    print(f'Post id range: {min_post_id} - {max_post_id}')

    account_ids = set()
    for post in posts:
        account_ids.add(post['uploader_id'])

    print(f'Start processing accounts Count: {len(account_ids)}')
    process_accounts(list(account_ids))

    print('Start processing posts')
    process_posts(posts)

    tag_names = set()
    for post in posts:
        for tag_name in post['tag_string'].split(' '):
            tag_names.add(tag_name)

    print(f'Start processing tags Count: {len(tag_names)}')
    tag_name_ids = process_tags(list(tag_names))

    print('Start processing post_tags')
    process_post_tags(posts, tag_name_ids)

    print('Done')

# 6331972