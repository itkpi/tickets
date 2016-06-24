var myDashboard = new Dashboard();
//myDashboard.addWidget('issuedticketsWidget', 'Number', {
//    getData: function () {
//        var self = this;
//        Dashing.utils.get('issuedtickets_widget', function(data) {
//            $.extend(self.scope, data);
//        });
//    },
//    interval: 10000
//});

myDashboard.addWidget('daysWidget', 'Graph', {
    getData: function () {
        var self = this;
        Dashing.utils.get('days_widget', function(data) {
            $.extend(self.scope, data);
        });
    },
    interval: 30000
});

myDashboard.addWidget('peopleWidget', 'List', {
    getData: function () {
        var self = this;
        Dashing.utils.get('people_widget', function(data) {
            $.extend(self.scope, data);
        });
    },
    interval: 30000,
    rows: 2,
});

myDashboard.addWidget('todayWidget', 'List', {
    row: 1,
    getData: function () {
        var self = this;
        Dashing.utils.get('today_widget', function(data) {
            $.extend(self.scope, data);
        });
    },
    interval: 3000
});



myDashboard.addWidget('countersWidget', 'Number', {
    getData: function () {
        var self = this;
        Dashing.utils.get('counters_widget', function(data) {
            $.extend(self.scope, data);
        });
    },
    interval: 3000
});

myDashboard.addWidget('allticketsWidget', 'Knob', {
    getData: function () {
        var self = this;
        Dashing.utils.get('alltickets_widget', function(data) {
            $.extend(self.scope, data);
        });
    },
    interval: 3000
});

myDashboard.addWidget('tickettypesWidget', 'List', {
    row: 1,
    getData: function () {
        var self = this;
        Dashing.utils.get('tickettypes_widget', function(data) {
            $.extend(self.scope, data);
        });
    },
    interval: 30000
});
