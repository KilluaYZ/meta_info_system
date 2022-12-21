const state = {
    tagpresetParam:{},
    tagneedRunPreset:false
}

const mutations = {
    setpresetParam: (state,preload) => {
        state.tagpresetParam = preload
        if(state.tagpresetParam != undefined)
            state.tagneedRunPreset = true;
        console.log('传递初始化数据')
        console.log(state.tagpresetParam)
        console.log(state.tagneedRunPreset)
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