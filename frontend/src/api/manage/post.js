import request from '@/utils/request'
import { useMock } from '@/settings'
import {getMockPostData,UpdateData,DelData,AddData} from '@/mock/data'

//添加标签
export function addPost (payload) {
    const data = payload;
  
    return false ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(AddData)
        },100)
      }) : request({
      url: '/post/add',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
}

//删除标签
export function delPost (payload) {
    const data = payload;
  
    return false ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(DelData)
        },100)
      }) : request({
      url: '/post/del',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
}
  
//修改标签
export function updatePost (payload) {
    const data = payload;
  
    return false ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(UpdateData)
        },100)
      }) : request({
      url: '/post/update',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
}

//查询标签
export function getPost(payload) {
    
    if(payload.sortMode){
      if(payload.sortMode=='Hot'){
        payload.sort={
          sortAttr:'postPopularity',
          mode:'desc'
        }
      }else if(payload.sortMode=='New'){
        payload.sort={
          sortAttr:'postTime',
          mode:'desc'
        }
      }
    }
    
    const data = payload;
  
    return false ? getMockPostData(payload) : request({
      url: '/post/get',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
  
}