const state = {
    postpresetParam:{},
    postneedRunPreset:false
}

const mutations = {
    setpresetParam: (state,preload) => {
        state.postpresetParam = preload
        if(state.postpresetParam != undefined)
            state.postneedRunPreset = true;
        console.log('���ݳ�ʼ������')
        console.log(state.postpresetParam)
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