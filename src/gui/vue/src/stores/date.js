import {defineStore} from 'pinia'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

export const useDate = defineStore({
    id: 'date',
    
    state: () => ({
        currentDate: Date.now(),
    }),

    actions: {
        updateCurrentDate() {
            this.currentDate = Date.now()
        },

        fromNow(date) {
            return dayjs(date).from(this.currentDate)
        },
    },
})
