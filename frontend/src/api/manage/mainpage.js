import request from '@/utils/request'
import { useMock } from '@/settings'
import {HotTagsData,NewTagsData,HotPostsData,NewPostsData} from '@/mock/mainpagedata'

export function getHotTags(payload){
    const data = payload;
    return  useMock ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(HotTagsData)
        },100)
      }) : request({
        url: '/getHotTags',
        headers: {
          isToken: false
        },
        method: 'post',
        data: data.HotTagsNum
      })
}

export function getNewTags(payload){
    const data = payload;
    return  useMock ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(NewTagsData)
        },100)
      }) : request({
        url: '/getNewTags',
        headers: {
          isToken: false
        },
        method: 'post',
        data: data.NewTagsNum
      })
}

export function getHotPosts(payload){
    const data = payload;
    return  useMock ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(HotPostsData)
        },100)
      }) : request({
        url: '/getHotPosts',
        headers: {
          isToken: false
        },
        method: 'post',
        data: data.HotPostsNum
      })
}

export function getNewPosts(payload){
    const data = payload;
    return  useMock ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(NewPostsData)
        },100)
      }) : request({
        url: '/getNewPosts',
        headers: {
          isToken: false
        },
        method: 'post',
        data: data.NewPostsNum
      })
}