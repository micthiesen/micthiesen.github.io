'use strict';

var mic = {
  initFns: {
    // setUpContsScrolling: function() {
    //   var currentPage = 0;
    //   var loadingPage = false;
    //
    //   var getDistToBottom = function() {
    //     return $(document).height() - ($(window).scrollTop() + $(window).height());
    //   };
    //
    //   var getNextPage = function() {
    //   };
    //
    //   $(window).scroll(function() {
    //     if (getDistToBottom() < 600) {
    //       // TODO: implement once you actually have enough posts to justify it
    //     }
    //   });
    // },
    setUpDynamicDates: function() {
      var isElemDateValid = function(index, elem) {
        return moment($(elem).attr('data-d-date')).isValid();
      };

      var updateElemDate = function(index, elem) {
        var $elem = $(elem);
        var dateString = moment($elem.attr('data-d-date')).fromNow();
        $elem.text(dateString);
      };

      var $dateElems = $('[data-d-date]').filter(isElemDateValid);
      $dateElems.each(updateElemDate);
    }
  }
};

$(document).ready(function init(argument) {
  $.each(mic.initFns, function(index, hookFn) { hookFn(); }); // initialize
});
