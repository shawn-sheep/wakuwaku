import router from "@/router";
import store from "@/store";
import API from "@/plugins/axios"

export class tag {
    id : string;
    name : string;
    count : number;
    type: string;
    constructor() {
        this.id = ''
        this.name = ''
        this.count = 0
        this.type = ''
    }
}

export class image {
    id : string;
    src : string;
    description : string;
    tags: tag[];
    width: number;
    height: number;
    constructor() {
        this.id = ''
        this.src = ''
        this.description = ''
        this.tags = []
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

export const showImage = async (pre_img : image) => {
    store.state.displayImage = await getImageByID(pre_img.id)
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

    const img = new image()
    await API.get('/posts/' + id).then((res) => {
        console.log(res)
        if (res.status === 200) {
            const res_img = res.data.images[0]
            img.id = res.data.post_id
            img.src = res_img.sample_url
            img.description = res.data.title
            img.tags = res.data.tags
            img.width = res_img.width
            img.height = res_img.height
        }
    }).catch((res) => {
        console.log("get image error")
    })
    return img
}

export const getImages = async (params : any) => {
    const imgs : image[] = []
    await API.get('/posts', { params }).then((res) => {
        console.log(res)
        if (res.status === 200) {
            for (const i in res.data) {
                const res_data = res.data[i]
                const img = new image()
                img.id = res_data.post_id
                img.src = res_data.preview_url
                img.description = res_data.title
                img.width = res_data.width
                img.height = res_data.height
                imgs.push(img)
            }
        }
    }).catch((res) => {
        console.log("get image error")
    })
    return imgs
}
