/**
 * Created by liu on 6/1/17.
 */

var app = new Vue({
    el: "#app",

    data: {
        message: "",
        start: 0,
        end: 1,
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
        datatable: []
    },

    computed: {
        selected() {
            return this.datatable.filter(function (obj) {
                return obj.selected
            }).map(function (obj) {
                return obj.id
            })
        }
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
                self.datatable =  response.data
                self.datatable.forEach(function(obj) { obj.selected = false })
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
        },
        end: function() {
            this.showtable()
        }
    },

    mounted: function () {
        this.start=1
        this.end = 5
    }

})