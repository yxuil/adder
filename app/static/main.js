/**
 * Created by liu on 6/1/17.
 */

Vue.use(Vuetable);

var app = new Vue({
    el: "#app",

    data: {
        message: "",
        start: 0,
        end: 10,
        queryparams: {},
        numbers: "",
        columns: [
            "__checkbox",
            {
                name: "id",
                title: "ID"
            }, {
                name: "initialy",
                title: "Original"
            }, {
                name: "plusone",
                title: "Plus One"
            }, {
                name: "timestwo",
                title: "Then Double"
            }],
        datatable: [
            {"id": 1, "initialy": 25, "plusone": 26, "timestwo": 52},
            {"id": 2, "initialy": 25, "plusone": null, "timestwo": null},
            {"id": 3, "initialy": 34, "plusone": null, "timestwo": null},
            {"id": 4, "initialy": 35, "plusone": null, "timestwo": null},
            {"id": 5, "initialy": 38, "plusone": null, "timestwo": null},]
    },

    computed: {
    },

    methods: {
        load: function() {
            var self = this
            self.message = "Loading"
            axios({
                method: 'post',
                url:'/api/load',
                data: {
                    "num": self.numbers
                }
            }).then( function(res){
                self.message = "Loaded number: "+ res.data["new added num"]
                self.end = res.data["total records"]
            })
        },
        showtable: function() {
            var self = this
            axios({
                method: "post",
                url: "/api/numbers",
                data: {
                    "start":self.start,
                    "end":self.end
                }
            }).then(function(response) {
                self.datatable = response.data
            })
        },
        add: function() {
            axios.post("/api/" + id1 + "/add", {
                "num": Vue.numbers
            })
        },
        double: function() {
            axios.post("/api/" + id1 + "/double", {
                "num": Vue.numbers
            })},
    },

    watch: {
        start: function() {
            this.showtable()
            this.$refs.vuetable.refresh()
        },
        end: function() {
            this.showtable()
            this.$refs.vuetable.refresh()
        }
    },

    ready: function () {
        this.showtable()
        this.queryparams={
                "start":self.start,
                "end":self.end
            }
        alert(this.datatable)
    }

})