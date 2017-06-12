var app = angular.module('demoApp', []);

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

app.controller('demoCtrl', ['$scope', '$http', '$window', 'Scopes',  function userCtrl ($scope, $http, $window, Scopes){
	$http.post('http://localhost:8000/nestedcomments/get_comments/').success(function(data){
		$scope.comments = JSON.parse(data);
		console.log($scope.comments);
	}).error(function(data){
		console.log("ERROR");
	});


	$scope.add_comment = function (index){
		if(index==0){
			comment = $scope.comment0;
			$post_data = {comment: comment};
			$http.post('http://localhost:8000/nestedcomments/add_comment/', $post_data).success(function(data){
				$scope.comments.push({comment: comment, comment_type: 0, id: data,
					days: 0, hours: 0, minutes: 0, depth:0});
			}).error(function(data){
				console.log("ERROR");
			});
		}
	}

	$scope.add_nestedcomment = function (index, comment_id){
		comment = angular.element('#comment-'+comment_id).val();
		$post_data = {parent_id:comment_id, comment: comment};
		$http.post('http://localhost:8000/nestedcomments/add_nestedcomment/', $post_data).success(function(data){
			var temp_comments = $scope.comments;
			var comments_counter = 0;
			var new_comment_added = false;
			$scope.comments = [];
			for (var i = 0; i < temp_comments.length+1; i++) {
				if(!new_comment_added && i>index && 
					(temp_comments[i].depth<temp_comments[i-1].depth || temp_comments[i].depth == temp_comments[index].depth)){
					$scope.comments.push({comment: comment, comment_type: 1, id: data,
						days: 0, hours: 0, minutes: 0, depth:temp_comments[index].depth+1});
					new_comment_added = true;
				}
				else
					$scope.comments.push(temp_comments[comments_counter++]);
			}
			$scope.$apply();
		}).error(function(data){
			console.log("ERROR");
		});
	}

}]);