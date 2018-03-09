var lodash = require('./lodash.min.js');

var BASE_URL = window.location.origin + '/shops/';
var bus = new Vue();

var Shop = {
    template: '#shop',
    props: ['title', 'url', 'preferred', 'httpConfig'],
    methods: {
        like_shop: function () {
            var vm = this;
            axios.put(vm.url + 'like/', {}, vm.httpConfig)
                .then(function (response) {

                });

            bus.$emit('like', {title: this.title,
                                url: this.url
                               });

        },
        unlike_shop: function () {
            var vm = this;
            axios.put(vm.url + 'unlike/', {}, vm.httpConfig)
                .then(function (response) {

                });

            bus.$emit('unlike', {title: this.title,
                                url: this.url
                               });

        }
    }
};

var Shops = {
    template: '#shops',
    props: {
        shops: [],
        preferred: false,
        httpConfig: {}
    },
    mounted: function() {
        vm = this;
        bus.$on('like', function (shop) {
            vm.shops = lodash.filter(vm.shops, function(item) {
                return item.url != shop.url;
            });
        });
        bus.$on('unlike', function (shop) {
            vm.shops = lodash.filter(vm.shops, function(item) {
                return item.url != shop.url;
            });
        });
    },
    computed: {
        rows_of_four: function () {
            return lodash.chunk(this.shops, 4);
        }
    },
    methods: {
        booyaSucka: function (payload) {
            console.log(payload);
        }
    }
};

var Login  = {
    template: '#login',
    data: function () {
        return {
            email: 'admin@example.com', //FIXME!!
            password: 'insecure'
        };
    },
    props: ['authUrl'],
    methods: {
        perform_login: function () {
            var cm = this;
            axios.post(cm.authUrl, {
                email: cm.email,
                password: cm.password
            })
                .then(function (response) {
                    cm.$emit('authenticated', response.data.auth_token);
                });
        }
    }
};

Vue.component("shop", Shop);
Vue.component("shops", Shops);
Vue.component("login", Login);


new Vue({
    el: '#app',
    data: {
        all_shops: [],
        user: {
            is_superuser: false,
            id: 0,
            email: '',
            url: '',
            shops: []
        },
        httpConfig: {
            headers: {
                Accept: 'application/json',
                Authorization: ''
            }
        },
        active_component: 'app-login'
    },
    mounted: function () {
        this.active_component = 'app-login';
    },
    methods: {
                booyaSucka: function (payload) {
            console.log(payload);
                },

        login: function (payload) {
            var vm = this;
            vm.httpConfig.headers.Authorization = 'Token ' + payload;
            axios.get(BASE_URL + 'auth/me/', vm.httpConfig)
                .then(function (response) {
                    vm.user.id = response.data.id;
                    vm.user.email = response.data.email;
                    vm.user.url = BASE_URL + 'api/users/' +
                        vm.user.id + "/";

                    axios.get(vm.user.url, vm.httpConfig)
                        .then(function (rsp) {
                            vm.user.is_superuser = rsp.data.is_superuser;
                            vm.user.shops = rsp.data.shops;
                        });
                });
            return this.view_all_shops();
        },
        logout: function () {
        },
        view_all_shops: function () {
            this.get_shops();
            return this.active_component = 'app-all-shops';
        },
        view_preferred_shops: function () {
            this.get_user_shops();
            return this.active_component = 'app-preferred-shops';
        },
        admin_settings: function () {
            return this.active_component = 'app-admin-area';
        },
        get_shops: function () {
            var vm = this;
            axios.get(BASE_URL + 'api/shops/', vm.httpConfig)
                .then(function (response) {
                    vm.all_shops = response.data;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        get_user_shops: function () {
            console.log('fetching user shops');
            var vm = this;
            axios.get(this.user.url + 'shops/', vm.httpConfig)
                .then(function (response) {
                    vm.user.shops = response.data;
                })
                .catch(function (error) {
                    console.log(error);
                });
        },
        promote_user: function (user) {
        },
        demote_user: function (user) {
        }
    }
});
