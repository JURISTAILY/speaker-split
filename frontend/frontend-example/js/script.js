
var app = angular.module('exampleApp', []);

app.controller('progressController', function ($scope, $http, $window, $q) {

    $scope.info = {};
    $scope.info.description = "";
    $scope.info.progress = 0;

    $scope.calcProgress = function () {
        $scope.info.progress = $scope.info.description.length / 100 * 100;
    };


});
