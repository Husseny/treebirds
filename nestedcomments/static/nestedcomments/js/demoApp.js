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

	$scope.add_comment = function (index){
		if(index==0){
			comment = $scope.comment0;
			$post_data = {comment: comment};
			$http.post(site_url+'nestedcomments/add_comment/', $post_data).success(function(data){
				if(data != -1){
					$scope.comments.push({comment: comment, comment_type: 0, id: data,
						days: 0, hours: 0, minutes: 0, depth:1, show_reply_box: 0, time_message: "a while"});
					// The scope method refresh_comments() can replace the above line of code to refresh the comments 
					// listed in the html, with the cost of a request to the server
					// $scope.refresh_comments();
					$scope.comment0 = '';
				}
			}).error(function(data){
				console.log("ERROR");
			});
		}
	};

	$scope.add_nestedcomment = function (index, comment_id){
		comment = angular.element('#comment-'+comment_id).val();
		$post_data = {parent_id:comment_id, comment: comment};
		$http.post(site_url+'nestedcomments/add_nestedcomment/', $post_data).success(function(data){
			if(data != -1){
				$scope.refresh_comments();
				$scope.comments[index].show_reply_box = 0;
				angular.element('#comment-'+comment_id).val('');
			}
		}).error(function(data){
			console.log("ERROR");
		});
	};

	$scope.delete_comment = function(index, comment_id){
		$post_data = {comment_id:comment_id};
		$http.post(site_url+'nestedcomments/delete_comment/', $post_data).success(function(data){
			if(data != -1)
				$scope.refresh_comments();
		}).error(function(data){
			console.log("ERROR");
		});
	};

	$scope.refresh_comments_reply_box = function(index){
		for (var i = 0; i < $scope.comments.length; i++)
			if(i == index)
				$scope.comments[i].show_reply_box = ! $scope.comments[i].show_reply_box;
			else
				$scope.comments[i].show_reply_box = 0;
		return true
	};

	$scope.refresh_comments = function(){
		$http.post(site_url+'nestedcomments/get_comments/').success(function(data){
			$scope.comments = JSON.parse(data);
			console.log($scope.comments);
		}).error(function(data){
			console.log("ERROR");
		});
	};

	$scope.refresh_comments();

}]);