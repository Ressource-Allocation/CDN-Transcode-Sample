"use strict";

$(".top-bar").on(":initpage", function (e) {
    $("#setting").find("[ui-header-setting-user] input").val(settings.user());
    $(this).find("[user-name-menu]").text(settings.user());
});

$("#setting").find("form").submit(function () {
    var page = $(this);

    var user = page.find("[ui-header-setting-user] input").val().toLowerCase();
    settings.user(user);
    $(".top-bar").find("[user-name-menu]").text(user);
    $("#player").trigger(":update");
    return false;
});

var settings = {
    user: function (name) {
        if (typeof name != "undefined") localStorage.user = name;
        return typeof localStorage.user != "undefined" ? localStorage.user : "guest";
    },
}


//upload
$("#upload .choose-file").click(
    function () {
        $("#upload .input_file").trigger('click')
    }
)

$("#upload .input_file").change(
    function () {
        var filePath = $("#upload .input_file").val()
        var pos = filePath.lastIndexOf("\\");
        var fileName = filePath.substring(pos + 1);
        $("#upload .choose-file .input-group-field").val(fileName)
    }
)

$("#upload").find("form .button").click(function () {
    if (!$("#upload .input_file").val()) {
        return false
    }
    if (!(document.querySelector("#upload .input_file").files[0].name.endsWith('.mp4'))) {
        $(".flex-center").show()
        $(".flex-center h6").html("Please choose mp4 file")
        $(".flex-center .input-group-bar").hide()
        return false
    } else {
        upload()
    }
});

//upload-offline
$("#upload-offline .choose-file").click(
    function () {
        $("#upload-offline .input_file").trigger('click')
    }
)

$("#upload-offline .input_file").change(
    function () {
        var filePath = $("#upload-offline .input_file").val()
        var pos = filePath.lastIndexOf("\\");
        var fileName = filePath.substring(pos + 1);
        $("#upload-offline .choose-file .input-group-field").val(fileName)
    }
)

$("#upload-offline").find("form .button").click(function () {
    if (!$("#upload-offline .input_file").val()) {
        return false
    }
    if (!(document.querySelector("#upload-offline .input_file").files[0].name.endsWith('.mp4'))) {
        $(".flex-center").show()
        $(".flex-center h6").html("Please choose mp4 file")
        $(".flex-center .input-group-bar").hide()
        return false
    } else {
        upload(true)
    }
});

function upload(isOffline = false) {
    $(".flex-center").show()
    $(".flex-center .input-group-bar").show()
    const LENGTH = 1024 * 1024 * 10;
    var timeStamp = new Date().getTime();
    if (isOffline) {
        var fileName = $("#upload-offline .choose-file .input-group-field").val();
        var type = $("#upload-offline select").val();
    } else {
        var fileName = $("#upload .choose-file .input-group-field").val();
    }
    var file = document.querySelector(isOffline ? '#upload-offline .input_file' : '#upload .input_file').files[0];
    var totalSize = file.size;
    var start = 0;
    var end = start + LENGTH;
    var fd = null;
    var blob = null;
    var xhr = null;
    var sum = Math.ceil(totalSize / LENGTH)
    var count = 0
    var timer = setInterval(function () {
        if (start < totalSize) {
            fd = new FormData();
            xhr = new XMLHttpRequest();
            if (isOffline) {
                xhr.open('POST', '/upload-offline/', false);
                fd.append('type', type);
            } else {
                xhr.open('POST', '/upload/', false);
            }
            blob = file.slice(start, end);
            fd.append('file', blob);
            fd.append('fileName', fileName);
            fd.append('timeStamp', timeStamp);
            fd.append('count', String(count));
            if (end >= totalSize) {
                fd.append('uploadStatus', 'end')
            }
            xhr.send(fd);
            console.log(xhr.status)
            if (xhr.status !== 200) {
                console.log("error" + xhr.status)
                $(".flex-center h6").html("Error, Please try again")
                $(".flex-center .input-group-bar").hide()
                clearInterval(timer);
                return false
            }
            count += 1
            $(".flex-center h6").html("Upload " + parseInt(count * 100 / sum) + "%")
            $(".flex-center .bar").width(parseInt(count * 100 / sum) + "%")
            start = end;
            end = start + LENGTH;
        } else {
            $(".flex-center h6").html("Upload success")
            setTimeout(function () {
                $(".flex-center h6").html("Upload 0%")
                $(".flex-center .bar").width("0%")
                $(".flex-center").hide()
                $("#upload .input_file").val('')
                $("#upload .choose-file .input-group-field").val('')
                $("#setting").find("form").submit();
                $(".reveal-overlay").trigger('click');
            }, 1000)
            clearInterval(timer);
        }
    }, 100)
}

//clear
$("#clear").find("form .button").click(function () {
    $("#clear-result").empty()

    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/clear/");
    xhr.responseType = "json"

    xhr.onload = function () {
        if (xhr.status !== 200) {
            console.log("clear request error " + xhr.status);
            $("#clear-result").append("<p>Error, Please try again</p>");
            return;
        }

        const data = xhr.response
        if (Object.keys(data).length === 0) {
            $("#clear-result").append("<p>Nothing to clear</p>");
            return;
        }

        $("#clear-result").append("<p>Result:</p>")
        $("#clear-result p").append("<ul></ul>")
        for (let i in data) {
            $("#clear-result ul").append(`<li>${data[i]["type"]}/${data[i]["file"]}: ${data[i]["zk"]["state"]}</li>`)
        }
    };

    xhr.send()
})
