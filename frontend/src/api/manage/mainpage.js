import {getMockHotTags,getMockNewTags,getMockHotPosts,getMockNewPosts} from '@/mock/mainpagedata'

export function getHotTags(payload){
    const data = payload;
    return getMockHotTags(payload)
}

export function getNewTags(payload){
    const data = payload;
    return getMockNewTags(payload)
}

export function getHotPosts(payload){
    const data = payload;
    return getMockHotPosts(payload)
}

export function getNewPosts(payload){
    const data = payload;
    return getMockNewPosts(payload)
}