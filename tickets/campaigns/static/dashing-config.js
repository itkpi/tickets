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

myDashboard.addWidget('tickettypesWidget', 'List', {
    getData: function () {
        var self = this;
        Dashing.utils.get('tickettypes_widget', function(data) {
            $.extend(self.scope, data);
        });
    },
    interval: 10000
});

myDashboard.addWidget('countersWidget', 'Knob', {
    getData: function () {
        var self = this;
        Dashing.utils.get('counters_widget', function(data) {
            $.extend(self.scope, data);
        });
    },
    interval: 3000
});

myDashboard.addWidget('daysWidget', 'Graph', {
    getData: function () {
        var self = this;
        Dashing.utils.get('days_widget', function(data) {
            $.extend(self.scope, data);
        });
    },
    interval: 10000
});
