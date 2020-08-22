<template>
    <LoggedinSidebarTemplate page_name="research">
        <template v-slot:main-content>
            <div class="max-w-xl mx-auto mb-10 sm:mb-0 min-h-screen">
                <div class="max-w-xl mx-auto lg:px-4">
                <div id="explanation" ref="explanation" class="relative w-full" tabindex="-1" style="top: -4.2rem;"></div>
                    <section class="table-content">
                        <table>
                            <thead>
                                <th>Study</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </thead>
                            <tbody id="core-data" class="sect">
                                <tr v-for="(study, index) in studies" :key="index">
                                    <td class="name-column">
                                        <strong>
                                            <h1>{{study.title}}</h1>
                                        </strong>
                                        <h4>Run by SanoGenetics</h4>
                                    </td>
                                    <td class="enrolled-column">
                                        <h1 class="enrolled-text" v-if="user_studies.find(row => row.id === study.id)">Enrolled</h1>
                                        <!-- <button class="enrolled-btn in-progress" v-if="index === 1">In Progress</button> -->
                                        <button class="enrolled-btn complete" v-if="user_studies.find(row => row.id === study.id)">Complete</button>
                                        <h1 v-else class="enrolled-text">Not Enrolled</h1>
                                    </td>
                                    <td class="action-column">
                                        <button @click="unenroll(study)" v-if="user_studies.find(row => row.id === study.id)" class="sano-btn text-sano-burgandy bg-sano-pink border-sano-pink sano-btn-narrow">
                                            Leave Study
                                        </button>
                                        <button v-else @click="enroll(study)" class="sano-btn text-white border-sano-red-orange sano-btn-narrow bg-sano-red-orange">
                                            Join Study
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </section>
                </div>
            </div>
        </template>
        <template v-slot:sidebar-content>
        </template>
    </LoggedinSidebarTemplate>
</template>

<script>

import LoggedinSidebarTemplate from "@/layouts/LoggedinSidebarTemplate";
import axios from 'axios'
import Vue from 'vue'
import store from '@/store/store.js'

export default {
    name: "Research",
    components: {
        LoggedinSidebarTemplate,
    },

    data() {
        return {
            studies: {}
        }
    },

    computed: {
        user_studies() {
            return store.state.studies
        }
    },

    created()
    {
        // this function gets the studies the authenticated user has subscribed to, so we know whether to put them as assigned or not in our list.
        axios.get('/user/studies')
        .then(res => {
            store.commit('setStudies', res.data)
        })
        .catch(error => {
            console.error(error.response)
        })

        axios.get('/studies')
        .then(res => {
            this.studies = res.data
        })
        .catch(error => {
            console.error(error.response)
        })
    },

    methods: {
        unenroll(study)
        {
            axios.post('/enroll/remove', {
                study_id: study.id
            })
            .then(res => {
                Vue.toast({ type: "success", title: `Study removed successfully` });
                // the below process will update the attached studies as they are displayed live on the page.
                store.commit('removeStudy', study)
            })
            .catch(error => {
				Vue.toast({ type: "error", title: `Failed to remove study: ${error.response.status}` });
                console.error(error.response)
            })
        },
        enroll(study)
        {
            axios.post('/enroll', {
                study_id: study.id
            })
            .then(res => {
                Vue.toast({ type: "success", title: `Enrolled successfully` });
                // as with unenrolling this now shows the course as being enrolled to. this will synchronise with the studies_users table.
                store.commit('addStudy', study)
            })
            .catch(error => {
				Vue.toast({ type: "error", title: `Failed to remove study: ${error.response.status}` });
                console.error(error.response)
            })
        }
    }
};
</script>

<style scoped lang="scss">
.mobile-sticky {
    top: 1rem;
}

.red-btn {
    background-color: #F75338;
}

.enrolled-text {
    color: #F75338;
}

.table-content {
    padding: 30px 0px;
}

.table-content th {
    text-transform: uppercase;
}

.sect tr {
    border-style: solid;
    border-color: #F7D2D2;
    border-width: thin;
    padding: 15px;
}

.in-progress {
    background-color: blue;
}

.complete {
    background-color: green;
}

.enrolled-btn {
    border-radius: 14px;
    color: #fff;
    margin: 3px 0px;
    padding: 0px 15px;
}

.sect td {
    padding: 15px;
}

.action-column {
    width: 21%;
    text-align: center;
}

.name-column {
    width: 50%;
}



.sect {
    @apply relative mt-6 mx-4 px-4 py-6 border border-sano-pink rounded overflow-hidden bg-white;
    @media (min-width: 992px) {
        @apply p-8 mx-0;
    }
}

@media (max-width: 575px) {

    .sect tr {
        display: grid;
    }

    .table-content th {
        display: none;
    }

    .enrolled-text {
        font-size: 30px;
    }
    
    .enrolled-column {
        order: 0;
        width: 100%;
        display: flex;
        justify-content: space-between;
    }

    .name-column {
        order: 1;
        width: 100%;
    }

    .name-column h1 {
        font-size: 20px;
    }

    .action-column {
        order: 2;
        width: 100%;
        display: grid;
    }

    .mobile-sticky {
        @apply sticky bg-white -ml-4 px-4 border-b border-sano-pink;
        z-index: 99;
        top: 0;
        width: calc(100% + 2rem);
    }

    .sano-toggle-label.sano-toggle-label {
        padding: 0 0.75rem;
    }
}
</style>
