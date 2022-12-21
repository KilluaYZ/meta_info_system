const state = {
    presetParam:{},
    needRunPreset:false
}

const mutations = {
    setpresetParam: (state,preload) => {
        state.presetParam = preload
        if(state.presetParam != undefined)
            state.needRunPreset = true;
        console.log('传递初始化数据')
        console.log(state.presetParam)
    }
}

const actions = {
    
}

export default {
    namespaced: true,
    state,
    mutations,
    actions
}