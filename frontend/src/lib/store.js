import { writable } from 'svelte/store'

//이름(key)과 초기값(initValue)을 입력받아 writable 스토어를 생성, 리턴하는 함수
const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key);
    //localStorage를 사용하여 지속성 가짐
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue);
    //localStorage에 해당 이름의 값이 있으면 초기값 대신 기존의 값으로 스토어 생성, 리턴
    //localStorage에 저장하는 값은 항상 문자열로 유지; 저장할 땐 JSON.stringify 읽을 땐 JSON.parse
    store.subscribe((val) => {
        //스토어에 저장된 값이 변경될 때 실행되는 콜백 함수
        //스토어 변수 값이 변경될 때 localStorage 값도 함꼐 변경 
        localStorage.setItem(key, JSON.stringify(val))
    });
    return store;
}

export const page = persist_storage("page", 0)
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false)
export const keyword = persist_storage("keyword", "")

////쓰기 가능한 스토어 변수 생성, writable(0)에서 0은 초깃값이 0