import router from "@/router";
import store from "@/store";
import API from "@/plugins/axios"

export class image {
    id : string;
    src : string;
    description : string;
    tags: string[];
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

export const goto = (url : string) => {
    if (url != null) router.push(url)
}

export const sleep = (time : number) => {
    return new Promise((resolve, reject) => {
        // eslint-disable-next-line @typescript-eslint/no-empty-function
        setTimeout(() => {}, time)
    })
}

export const showImage = (img : image) => {
    store.state.isDisplayImage = true
    store.state.displayImage = img
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
    for (const i in store.state.recommend) {
        if (store.state.recommend[i].id === id) {
            return store.state.recommend[i]
        }
    }
    return new image()
}
