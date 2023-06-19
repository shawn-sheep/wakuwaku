import router from "@/router";
import store from "@/store";
import API from "@/plugins/axios"

export class tag {
    tag_id : string;
    name : string;
    count : number;
    type: string;
    constructor() {
        this.tag_id = ''
        this.name = ''
        this.count = 0
        this.type = ''
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
    constructor() {
        this.account_id = ''
        this.content = ''
        this.date = ''
        this.img = new image()
        this.post_id = ''
        this.score = 0
        this.source = ''
        this.title = ''
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
    id: string;
    avatar: string;
    username: string;
    content: string;
    reply: comment[]
    constructor() {
        this.id = ''
        this.avatar = require('@/assets/img/user_avatar.jpg')
        this.username = 'Lierick'
        this.content = 'default comment\ndefault comment\ndefault comment'
        this.reply = []
    }
}

export const goto = (url : string, newTab=false, useRouter=true) => {
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

export const sleep = (time : number) => {
    return new Promise((resolve, reject) => {
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        setTimeout(() => {}, time)
    })
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
