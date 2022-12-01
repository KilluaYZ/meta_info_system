import request from '@/utils/request'
import { useMock } from '../settings'
import { TookenData,UserData,GetData,EditData,DelData,AddData } from '../mock/data'

//添加标签
export function addtag (payload) {
    const data = payload;
  
    return useMock ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(AddData)
        },100)
      }) : request({
      url: '/addtag',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
}

//删除标签
export function deltag (payload) {
    const data = payload;
  
    return useMock ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(DelData)
        },100)
      }) : request({
      url: '/deltag',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
}
  
//修改标签
export function edittag (payload) {
    const data = payload;
  
    return useMock ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(EditData)
        },100)
      }) : request({
      url: '/edittag',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
}

//查询标签
export function gettag(payload) {
    const data = payload;
  
    return useMock ? new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(GetData)
      },100)
    }) : request({
      url: '/gettag',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
  
}