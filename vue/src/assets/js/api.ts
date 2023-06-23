import router from "@/router";
import store from "@/store";
import API from "@/plugins/axios"

export class user {
    account_id : number;
    avatar_url : string;
    created_at : string;
    email : string;
    username : string;
    constructor() {
        this.account_id = 0
        this.avatar_url = require('@/assets/img/user_avatar.jpg')
        this.created_at = ''
        this.email = '3336970253@qq.com'
        this.username = 'Lierick'
    }
}

export class tag {
    tag_id : string;
    name : string;
    count : number;
    type: number;
    constructor() {
        this.tag_id = ''
        this.name = ''
        this.count = 0
        this.type = 0
    }
}

export class postPreview {
    account_id: string;
    content: string;
    date: string;
    img: image;
    post_id: string;
    score: number;
    source: string;
    title: string;
    image_count: number;
    constructor() {
        this.account_id = ''
        this.content = ''
        this.date = ''
        this.img = new image()
        this.post_id = ''
        this.score = 0
        this.source = ''
        this.title = ''
        this.image_count = 0
    }
}

export class postDetail {
    account_id: string;
    content: string;
    date: string;
    imgs: image[];
    post_id: string;
    score: number;
    source: string;
    title: string;
    tags: tag[]
    constructor() {
        this.account_id = ''
        this.content = ''
        this.date = ''
        this.imgs = [new image()]
        this.post_id = ''
        this.score = 0
        this.source = ''
        this.title = ''
        this.tags = []
    }
}

export class image {
    image_id : string;
    name : string;
    original_url : string;
    post_id: string;
    preview_url: string;
    sample_url: string
    width: number;
    height: number;
    constructor() {
        this.image_id = ''
        this.name = ''
        this.original_url = ''
        this.post_id = ''
        this.preview_url = ''
        this.sample_url = ''
        this.width = 512
        this.height = 512
    }
}

export class comment {
    comment_id: string;
    account_id: string;
    avatar_url: string;
    username: string;
    content: string;
    replies: comment[]
    constructor() {
        this.comment_id = ''
        this.account_id = ''
        this.avatar_url = require('@/assets/img/user_avatar.jpg')
        this.username = 'Lierick'
        this.content = 'default comment\ndefault comment\ndefault comment'
        this.replies = []
    }
}

export const getTags = async (count = 10) => {
    let out : tag[] = []
    await API.get('/tags', { params: { count } }).then((res) => {
        console.log(res)
        if (res.status === 200) {
            out = res.data
        }
    }).catch((err) => {
        console.log(err)
    })
    return out
}

export const getComments = async (post_id : string, page : number) => {
    let out : comment[] = []
    await API.get('/comments', { params: { post_id: post_id, page: page, per_page: 10 } }).then((res) => {
        console.log(res)
        if (res.status === 200) {
            out = res.data
        }
    }).catch((err) => {
        console.log(err)
    })
    return out
}


export const goto = (url : any, newTab=false, useRouter=true) => {
    if(newTab) {
        if(useRouter) {
            const href = router.resolve({
                path: url
            })
            window.open(href.href, '_blank')
        }
        else {
            window.open(url, '_blank')
        }
    } else {
        if (url != null) router.push(url)
    }
}

export const showPost = async (post : postPreview) => {
    store.state.displayPost = await getImageByID(post.post_id)
    store.state.isDisplayImage = true
}

export const login = async (form: { account: string, password: string }) => {
    const formData = new FormData()
    formData.append('username', form.account)
    formData.append('password', form.password)
    let out = ''
    await API.post('/login', formData).then((res) => {
        console.log(res)
        if (res.status === 200) {
            goto('/home')
        }
    }).catch((res) => {
        console.log(res)
        out = '登录时发生错误'
    })
    return out
}

export const register = async (form: { email: string, account: string, password: string }) => {
    const formData = new FormData()
    formData.append('email', form.email)
    formData.append('username', form.account)
    formData.append('password', form.password)
    let out = ''
    await API.post('/register', formData).then((res) => {
        console.log(res)
        if (res.status === 201) {
            goto('/enter')
        }
    }).catch((res) => {
        console.log(res)
        out = '注册时发生错误'
    })
    return out
}

export const logout = async () => {
    await API.get('/logout').then((res) => {
        console.log(res)
        goto('/enter')
    }).catch((res) => {
        console.log('logout failed')
    })
}

export const getUser = async () => {
    API.get('/user').then((res) => {
        console.log(res)
        store.state.user = res.data
        if (!store.state.user.avatar_url) store.state.user.avatar_url = require('@/assets/img/user_avatar.jpg')
    }).catch((res) => {
        console.log('get user information failed')
        goto('/enter')
    })
}

export const getUserByID = async (id : string) => {
    let out = new user()
    await API.get('/user/' + id).then((res) => {
        console.log(res)
        if (res.status === 200) {
            out = res.data
        }
    }).catch((res) => {
        console.log('get user information failed')
    })
    return out
}

export const checkLogin = async () => {
    API.get('user').then((res)=> {
        console.log(res)
        store.state.user = res.data
        if (!store.state.user.avatar_url) store.state.user.avatar_url = require('@/assets/img/user_avatar.jpg')
        goto('/home')
    }).catch((res) => {
        console.log('get user information failed')
    })
}

export const getImageByID = async (id : string) => {
    // for (const i in store.state.recommend) {
    //     if (store.state.recommend[i].id === id) {
    //         return store.state.recommend[i]
    //     }
    // }

    const post = new postDetail()
    await API.get('/posts/' + id).then((res) => {
        console.log(res)
        if (res.status === 200) {
            const res_data = res.data
            post.account_id = res_data.account_id
            post.content = res_data.content
            post.date = res_data.created_at
            post.post_id = res_data.post_id
            post.score = res_data.score
            post.source = res_data.source
            post.title = res_data.title
            post.imgs = res_data.images
            post.tags = res_data.tags
            // 对tags按照count排序
            post.tags.sort((a : any, b : any) => {
                return b.count - a.count
            })
        }
    }).catch((res) => {
        console.log("get image error")
    })
    return post
}

export const getPostPreviews = async (params : any) => {
    const postPreviews : postPreview[] = []
    await API.get('/posts', { params }).then((res) => {
        console.log(res)
        if (res.status === 200) {
            for (const i in res.data) {
                const res_data = res.data[i]
                const post = new postPreview()
                post.account_id = res_data.account_id
                post.content = res_data.content
                post.date = res_data.created_at
                post.img.preview_url = res_data.preview_url
                post.img.width = res_data.width
                post.img.height = res_data.height
                post.post_id = res_data.post_id
                post.score = res_data.score
                post.source = res_data.source
                post.title = res_data.title
                postPreviews.push(post)
            }
        }
    }).catch((res) => {
        console.log("get image error")
    })
    console.log(postPreviews)
    return postPreviews
}

export const autoComplete = async (q: string) => {
    const tags : tag[] = []
    await API.get('/autocomplete', { params: { q } }).then((res) => {
        console.log(res)
        if (res.status === 200) {
            for (const i in res.data.tags) {
                const res_data = res.data.tags[i]
                const tg = new tag()
                tg.tag_id = res_data.tag_id
                tg.name = res_data.name
                tg.count = res_data.count
                tg.type = res_data.type
                tags.push(tg)
            }
        }
    }).catch((res) => {
        console.log("get tag error")
    })
    return tags
}
