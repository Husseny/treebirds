var app = angular.module('homeApp', []);

app.config(function($interpolateProvider, $httpProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	$httpProvider.defaults.enctype="multipart/form-data";
});

app.factory('Scopes', function ($rootScope) {
	var mem = {};
 
	return {
		store: function (key, value) {
			$rootScope.$emit('scope.stored', key);
			mem[key] = value;
		},
		get: function (key) {
			return mem[key];
		}
	};
});

app.controller('homeCtrl', ['$scope', '$http', '$window', 'Scopes',  function userCtrl ($scope, $http, $window, Scopes){
	$scope.open_profile = function(index) {
		$http.post(site_url+'open_profile/', {index: index});
		switch(index){
			case 1: 
				$window.location.href='https://www.medium.com/@husseny';
				break;
			case 2: 
				$window.location.href='https://www.linkedin.com/in/husseny/';
				break;
			case 3: 
				$window.location.href='https://www.github.com/Husseny';
				break;
		}
	}
}]);