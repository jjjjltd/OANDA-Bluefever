var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue!',
        kpiData: undefined
    },
    methods: {
        // Note:  function needs to be declared async, otherwise the await(s) on the const(s) won't work.
        loadData: async function() {
            // console.log("Load Data Was Clicked!");
            const response = await fetch('data.json');
            const data = await response.json();
            // console.log(response);
            // console.log(data)
            this.kpiData = data;
            
        }
    }
})