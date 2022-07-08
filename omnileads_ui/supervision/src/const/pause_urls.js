export default {
    PauseList: '/api/v1/pauses',
    PauseCreate: '/api/v1/pauses/create/',
    PauseReactivate: (id) => `/api/v1/pauses/${id}/reactivate/`,
    PauseDelete: (id) => `/api/v1/pauses/${id}/delete`,
    PauseUpdate: (id) => `/api/v1/pauses/${id}/update/`,
    PauseDetail: (id) => `/api/v1/pauses/${id}`
};
