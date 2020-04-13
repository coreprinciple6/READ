const MIN_TIME = 3000;
BUTTON_SHOWN = false;
FILE_SHOWN = false;
STARTED_READING = false;
BEGIN_TIME = -1;
LAST_ELAPSED_TIME = 0;

function showFile(path){
    const iframe = document.createElement("iframe");
    iframe.src = path;
    iframe.id = "iframe_id";

    var iframe_div = document.getElementById("iframe_div");
    iframe_div.appendChild(iframe);
    FILE_SHOWN = true;

    const button_div = document.getElementById("button_div");
    button_div.remove();
    STARTED_READING = true;

    const leave_page_button_div = document.getElementById("leave_page_button_div");
    leave_page_button_div.style.display = "inline";
}

function showButton(){
    button = document.getElementById("button_div");
    button.style.display = "inline";
}

function removeFile(){
    const iframe = document.getElementById("iframe_div");
    iframe.remove();
    FILE_SHOWN = false;
}

function sendData(value){
    var form = document.myForm;
    form.querySelector("#elapsedInput").value = value/1000;
    form.submit();
}



function eye(){
    num_nulls = 0;
    prev_null_time = -1;
    DATA_SENT = false;
    webgazer.setGazeListener(function(data, elapsedTime) {
        if(BUTTON_SHOWN == false && webgazer.isReady() && elapsedTime > MIN_TIME){
            BUTTON_SHOWN = true;
            showButton();
        }
        if(STARTED_READING && BEGIN_TIME == -1){
            BEGIN_TIME = elapsedTime;
            num_nulls = 0;
        }
        if (data == null) {
            if(prev_null_time == -1){
                time_delta = elapsedTime;
            }
            else {
                time_delta = elapsedTime - prev_null_time;
            }
            //console.log(time_delta);
            prev_null_time = elapsedTime;
            if(time_delta < 3000){
                ++num_nulls;
            }
            else {
                num_nulls = 0;
            }
            //console.log(num_nulls);

            if(num_nulls >= 8 && STARTED_READING == true){
                console.log("No user");
                if(FILE_SHOWN){
                    removeFile();
                }
                if(STARTED_READING && !DATA_SENT){
                    LAST_ELAPSED_TIME = elapsedTime;
                    leave_page();
                }
                nums_nulls = 0;
            }
        }
        else {
            //console.log(elapsedTime);
        }
        LAST_ELAPSED_TIME = elapsedTime;
    }).begin().showPredictionPoints(false);
}

function leave_page(){
    DATA_SENT = true;
    sendData(LAST_ELAPSED_TIME - BEGIN_TIME);
}
eye();
