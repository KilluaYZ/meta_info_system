import request from '@/utils/request'

// 查询在线用户列表
export function list(query) {
  return request({
    url: '/user/online/list',
    method: 'get',
    params: query
  })
}

// 强退用户
export function forceLogout(tokenId) {
  return request({
    url: '/user/online/forceLogout',
    method: 'post',
    data:{
      token:tokenId
    }
  })
}
