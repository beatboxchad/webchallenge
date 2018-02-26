var lodash = require('./lodash.min.js');

var Shop = {
    template: '#shop',
    props: ['title', 'id', 'preferred']
};

var Shops = {
    template: '#shops',
    props: [ "dataUrl" ],
    data: function() {
        return {
            shops: []
        };
    },
    computed: {
        rowsOfFour: function() {
            return lodash.chunk(this.shops, 4);
        }
    },
    methods: {
        getShops: function() {
            axios.get(this.dataUrl)
                .then(function(response) {
                    this.shops = response.data;

                }.bind(this)
                     )
                .catch(function(error) {
                    console.log(error);
                });
        }
    },
    created: function() {
        this.getShops();

    }
};

Vue.component("shop", Shop);
Vue.component("shops", Shops);

var rootModel = {
    user: '',
    isAdminUser: false,
    activeComponent: 'app-all-shops'
};

var app = new Vue({
    el: '#app',
    data: rootModel,
    methods: {
        viewAllShops: function () {
            console.log('view all shops btn clicked');
            return this.activeComponent = 'app-all-shops';
        },
        viewPreferredShops: function () {
            console.log('view completed shops btn clicked');
            return this.activeComponent = 'app-preferred-shops';
        },
        adminSettings: function () {
            console.log("admin settings btn clicked");
        }
    }
});
