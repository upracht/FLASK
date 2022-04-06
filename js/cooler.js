
$(document).ready(function(){


  $("#PreButton").click(function(evnt){
    var newData = {"Pre": "do"};

    $.ajax({
        type: "POST",
        url: "/api/Pre",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(newData),
        dataType: "json"
    });
  });



  $("#PinnButton").click(function(evnt){
    var newData = {"Pinn": "do"};

    $.ajax({
        type: "POST",
        url: "/api/Pinn",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(newData),
        dataType: "json"
    });
  });



  $("#BaseButton").click(function(evnt){
    var newData = {"Base": "do"};

    $.ajax({
        type: "POST",
        url: "/api/Base",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(newData),
        dataType: "json"
    });
  });



  $("#OffButton").click(function(evnt){
    var newData = {"Off": "do"};

    $.ajax({
        type: "POST",
        url: "/api/Off",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(newData),
        dataType: "json"
    });
  });


  $("#ButtonDownload").click(function(evnt){
    var newData = {"stateDownload": "do"};

    $.ajax({
        type: "POST",
        url: "/api/stateDownload",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(newData),
        dataType: "json"
    });
    window.location.reload(true);
  });



});


