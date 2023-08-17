var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue!',
        kpiData: undefined
    },
    methods: {
        loadData: async function() {
            const response = await fetch('data.json');
            const data = await response.json();
            this.kpiData = data;            
        }
    }
})