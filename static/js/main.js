/**
 * Created by luiscunha on 9/5/16.
 */

(function(){
    console.log("Starting app")
})()

var api_host = "localhost" //"159.203.104.16"
var api_ip = 8871;
function showElem(elem){
    // Hide all elements, before showing the onde we intend to
    $.each($(".showhide"), function(k, v) { $(v).hide()})

    //show only the intended element
    switch(elem){
        case "my-requests":
            console.log("showing my-requests")
            $("#my-requests").show()
            break
        case "home":
            console.log("showing home")
            $("#home").show()
            break
        case "new-request":
            console.log("showing new-request")
            $("#new-request").show()
            break
        case "find":
            console.log("showing around me")
            $("#find").show()
            break
        default:
            console.log("nothing to show")
    }
}


function submitNewRequest(){
    /*
        Show flesh message, and remove it after a short time period
     */
    var id = $("#user_name").val()
    console.log(id)
    var url = "http://" + api_host + ":" + api_ip +"/match/request/" + data.user + "/" + id
    console.log(url)
    $.post( url)
          .done(function( data ) {
              result = JSON.parse(data);
              if (result.error){
                  var flash = result.error;
              }
              else {
                  flash = "Created New Request. Check back at later time for the user response and/or match result"
              }
              //{"_id": ["b8718dc1-6272-4d6b-b334-845a33e6ad1e"], "error": null}
              $("#flashM").text(flash)
            //alert( "Data Loaded: " + data );
              $("#flash_message").show()
                setInterval(function(){
                    $("#flash_message").hide()
                    //$("#user_name").val("")
                },10000)
                      });
}

function matchRequestResponse(id, user2, response){
    var url = "http://" + api_host + ":" + api_ip + "/match/response/" + id + "/" + user2 + "/" + response
    console.log(url)
    $.post( url)
        .done(function(data){
        console.log(data)
    })
}

var offset = 0;
function aroundMe(){
    var radius = $("#radius").val()
    var numberResults = $("#number_results").val()

    var url = "http://" + api_host + ":" + api_ip + "/match/geo/" + data.user
    console.log(url)
    var req = {
        "lat": null,
        "lon": null,
        "radius": radius,
        "offset": offset++ * 10,
        "limit": numberResults
    }

    $.ajax({
          url: url,
          type: 'post',
          dataType: 'json',
          success: function (data) {
              console.log(data);
              $("#aroundMeResults").empty()
              redoAroundMeResults(data)
          },
          data: JSON.stringify(req)
    });

}

function redoAroundMeResults(data){
    $.each(data, function(k, v){
        var elemString = "<li>User " + v.user_id + ". Distance: "+ Math.round(v.dist*100)/100 +" miles</li>"
        var elem = $(elemString)
        $("#aroundMeResults").append(elem)
        console.log(v)
    })



}
/*function matchRequestResponse(id, user2, response){
    var url = "http://" + api_host + ":" + api_ip + "/match/response/" + id + "/" + user2 + "/" + response
    console.log(url)
    var req = {
        "lat": null,
        "lon": null,
        "radius": 10,
        "offset": 0,
        "limit": 10
    }
            $.ajax({
                url: url,
                type: 'post',
                dataType: 'json',
                success: function (data) {
                    console.log(data);
                },
                data: req
        });



}
    */