const { createApp } = Vue;
createApp({
    data() {
        return {
            timetable: {}
        }
    },
    mounted() {
        fetch('/api/timetable')
            .then(res => res.json())
            .then(data => {
                this.timetable = data;
            });
    }
}).mount('#app');
