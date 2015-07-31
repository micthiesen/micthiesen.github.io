'use strict';

var mic = {
  initFns: {
    setUpContsScrolling: function() {
      var currentPage = 0;
      var loadingPage = false;

      var getDistToBottom = function() {
        return $(document).height() - ($(window).scrollTop() + $(window).height());
      };

      var getNextPage = function() {
        // TODO: implement once you actually have enough posts to justify it
      };

      $(window).scroll(function() {
        if (getDistToBottom() < 600) {
          console.log('load next page');
        }
      });
    }
  }
};

$(document).ready(function init(argument) {
  //$.each(mic.initFns, function(index, hookFn) { hookFn(); }); // initialize
});
