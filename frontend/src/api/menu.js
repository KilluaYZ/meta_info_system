import request from '@/utils/request'
import { MenuData } from '@/mock/data'
import { useMock } from '../settings'
// 获取路由
export const getRouters = () => {
  return request({
    url: 'auth/getRouters',
    method: 'get'
  })

  // return false ? new Promise((resolve,reject) => {
  //   setTimeout(()=>{
  //     resolve(MenuData)
  //   },100)
  // }): request({
  //     url: 'auth/getRouters',
  //     method: 'get'
  // })

}