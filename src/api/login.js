import request from '@/utils/request'
import { useMock } from '../settings'
import { TookenData,UserData } from '../mock/data'
// 登录方法
export function login(username, password, code, uuid) {
  const data = {
    username,
    password,
    code,
    uuid
  }

  return useMock ? new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve(TookenData)
    },100)
  }) : request({
    url: '/login',
    headers: {
      isToken: false
    },
    method: 'post',
    data: data
  })

}

// 注册方法
export function register(data) {
  return request({
    url: '/register',
    headers: {
      isToken: false
    },
    method: 'post',
    data: data
  })
}

// 获取用户详细信息
export function getInfo() {
  console.log('enter getInfo')
  return useMock ?
    new Promise((resolve, reject) => {
      setTimeout(() => {
        console.log('enter getInfo Promise')
        resolve(UserData)
      },100)
    })
    : request({
      url: '/getInfo',
      method: 'get'
    })
}

// 退出方法
export function logout() {
  return request({
    url: '/logout',
    method: 'post'
  })
}

// 获取验证码
export function getCodeImg() {
  return request({
    url: '/captchaImage',
    headers: {
      isToken: false
    },
    method: 'get',
    timeout: 20000
  })
}