import request from '@/utils/request'
import { MenuData } from '../mock/data'
// 获取路由
export const getRouters = () => {
  // return request({
  //   url: '/getRouters',
  //   method: 'get'
  // })

  return new Promise((resolve,reject) => {
    setTimeout(()=>{
      resolve(MenuData)
    },500)
  })
}