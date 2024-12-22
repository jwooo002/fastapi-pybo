import qs from "qs"
import { access_token } from "./store"
import { get } from 'svelte/store'
import { push } from 'svelte-spa-router'

const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)

    if(operation === 'login') {
        method = 'post'
        content_type = 'application/x-www-form-urlencoded'
        body = qs.stringify(params)
    }

    let _url = new URL(import.meta.env.VITE_SERVER_URL + url);
    if(method === 'get') { //=== 는 더 엄격한 같음(타입도)
        _url += "?" + new URLSearchParams(params)
    }
    console.log("Request URL:", _url);

    let options = { //js/ 중괄호 객체 key - value 쌍의 집합 저장 
        method: method, 
        headers: {
            "Content-Type": content_type
        }
    }

    const _access_token = get(access_token)
    if (_access_token) { //access token에 값이 있을 경우 HTTP헤더에Authorization항목 추가
        options.headers["Authorization"] = "Bearer " + _access_token//문자열에 띄어쓰기 해야함
    }

    if (method !== 'get') {
        options['body'] = body
    }

    fetch(_url, options)
        .then(response => {
            if(response.status === 204) {
                if(success_callback) { 
                    success_callback()
                }
                return
            }
            console.log("Response status:", response.status);
            response.json()
                .then(json => {
                    console.log("Response JSON:", json);
                    if(response.status >= 200 && response.status < 300) {  // 200 ~ 299
                        if(success_callback) {
                            success_callback(json)
                        }
                    }
                    //operation이 login이 아닌데 401이면 로그인이 필요한 상황
                    //operation이 로그인인 경우는 아이디나 비번 틀림
                    else if(operation !== 'login' && response.status === 401) {
                        //스벨트가 아니라 js라서 $기호 못씀 스토어 변수는 get, set 해야 함
                        access_token.set('')
                        username.set('')
                        is_login.set(false)
                        alert("Need to login")
                        push('/user-login')
                    }
                    else {
                        if (failure_callback) {
                            failure_callback(json)
                        }else {
                            alert(JSON.stringify(json))
                        }
                    }
                })
                .catch(error => {
                    console.error("Fetch error:", error);
                    alert(JSON.stringify(error))
                })
        })
}

export default fastapi
