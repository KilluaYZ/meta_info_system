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
        url: 'vis/getHotTags',
        headers: {
          isToken: false
        },
        method: 'post',
        data: data
    })
}

export function getNewTags(payload){
    const data = payload;
    return  useMock ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(NewTagsData)
        },100)
      }) : request({
        url: 'vis/getNewTags',
        headers: {
          isToken: false
        },
        method: 'post',
        data: data
      })
}

export function getHotPosts(payload){
    const data = payload;
    return  useMock ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(HotPostsData)
        },100)
      }) : request({
        url: 'vis/getHotPosts',
        headers: {
          isToken: false
        },
        method: 'post',
        data: data
      })
}

export function getNewPosts(payload){
    const data = payload;
    return  useMock ? new Promise((resolve, reject) => {
        setTimeout(() => {
          resolve(NewPostsData)
        },100)
      }) : request({
        url: 'vis/getNewPosts',
        headers: {
          isToken: false
        },
        method: 'post',
        data: data
      })
}