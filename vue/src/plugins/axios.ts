import axios from "axios";

const API = axios.create({
    baseURL: '/api',
    timeout: 2000,
    // headers: {
    //     'Content-Type': 'application/json'
    //     // 'Content-Type': 'multipart/form-data'
    // }
})

export default API
