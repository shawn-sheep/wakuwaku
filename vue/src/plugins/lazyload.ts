export default {
    install (app : any) {
        lazyload(app)
    }
}

const lazyload = (app:any) => {
    // 图片懒加载指令
    app.directive('lazyload', {
        mounted (el:any, binding:any) { // vue2.0 inserted vue3.0 mounted
            const observer = new IntersectionObserver(([{ isIntersecting }]) => {
                if (isIntersecting) { // isIntersecting判断是否进入视图
                    observer.unobserve(el) // 进入视图后，停止监听
                    el.onerror = () => { // 加载失败显示默认图片
                        console.log('error')
                    }
                    el.src = binding.value // 进入视图后，把指令绑定的值赋值给src属性，显示图片
                }
            }, {
                threshold: 0.01 // 当图片img元素占比视图0.01时 el.src = binding.value
            })
            observer.observe(el) //观察指令绑定的dom
        }
        // updated (el:any, binding:any) { // vue2.0 inserted vue3.0 mounted
        //     console.log('update',binding.value)
        //     const observer = new IntersectionObserver(([{ isIntersecting }]) => {
        //         if (isIntersecting) { // isIntersecting判断是否进入视图
        //             observer.unobserve(el) // 进入视图后，停止监听
        //             el.onerror = () => { // 加载失败显示默认图片
        //                 console.log('error')
        //             }
        //             el.src = binding.value // 进入视图后，把指令绑定的值赋值给src属性，显示图片
        //         }
        //     }, {
        //         threshold: 0.01 // 当图片img元素占比视图0.01时 el.src = binding.value
        //     })
        //     observer.observe(el) //观察指令绑定的dom
        // }
    })
}
