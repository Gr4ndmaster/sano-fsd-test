import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        menu_hidden: true,
        mobile_menu_hidden: true,
        studies: []
    },
    getters: {
        menu_hidden: (state) => state.menu_hidden
    },
    mutations: {
        setStudies(state, studies)
        {
            state.studies = studies
        },
        addStudy(state, study)
        {
            state.studies.push(study)
        },
        removeStudy(state, study)
        {
            let index = state.studies.indexOf(state.studies.find(row => row.id === study.id))
            state.studies.splice(index, 1)
        }
    },
    actions: {}
});
