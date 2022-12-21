import request from '@/utils/request'
import { useMock } from '@/settings'
import {getMockTagData,UpdateData,DelData,AddData,frontTagTreeData} from '@/mock/data'

//添加标签
export function addTag (payload) {
    const data = payload;
  
    return false ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(AddData)
        },100)
      }) : request({
      url: '/tag/add',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
}

//删除标签
export function delTag (payload) {
    const data = payload;
  
    return false ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(DelData)
        },100)
      }) : request({
      url: '/tag/del',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
}
  
//修改标签
export function updateTag (payload) {
    const data = payload;
  
    return false ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(UpdateData)
        },100)
      }) : request({
      url: '/tag/update',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
}

//查询标签
export function getTag(payload) {
  if(payload.sortMode){
      if(payload.sortMode=='Default'){
        payload.sort={
          sortAttr:'tagID',
          mode:'asc'
        }
      }else if(payload.sortMode=='Hot'){
        payload.sort={
          sortAttr:'tagPopularity',
          mode:'desc'
        }
      }else if(payload.sortMode=='New'){
        payload.sort={
          sortAttr:'createTime',
          mode:'desc'
        }
      }
    }
    const data = payload;
    return false ? getMockTagData(payload) : request({
      url: '/tag/get',
      headers: {
        isToken: false
      },
      method: 'post',
      data: data
    })
}

//获取前向标签路径
export function getFrontTagTree(payload) {
  const data = payload;

  return false ? new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve(frontTagTreeData)
    },100)
  }) : request({
    url: '/tag/getFrontTree',
    headers: {
      isToken: false
    },
    method: 'post',
    data: data
  })

}