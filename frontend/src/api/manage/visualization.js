import request from '@/utils/request'
import { useMock } from '../settings'
import {HotTagsData,NewTagsData,HotPostsData,NewPostsData} from '@/mock/mainpagedata'

export function getData(startdate,enddate){
    const data = {startDate:startdate,endDate:enddate};
    return  false ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(HotTagsData)
        },100)
      }) : request({
        url: 'vis/getHotTags',
        headers: {
          isToken: false
        },
        method: 'post',
        data: data
      })
}