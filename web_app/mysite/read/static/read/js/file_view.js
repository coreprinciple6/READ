const MIN_TIME = 3000;
FIRST_BUTTON_SHOWN = false;
STARTED_READING = false;
BEGIN_TIME = -1;
LAST_ELAPSED_TIME = 0;

function showFile(path){
    STARTED_READING = true;
    removeShowButton();

    const iframe = document.createElement("iframe");
    iframe.src = path;
    iframe.id = "iframe_id";

    var iframe_div = document.getElementById("iframe_div");
    iframe_div.appendChild(iframe);

    showLeaveButton();
}
function moveShowButton(){
    const button_div = document.getElementById("button_div");
}
function removeShowButton(){
    const button_div = document.getElementById("button_div");
    button_div.remove();
}
function showLeaveButton(){
    const leave_page_button_div = document.getElementById("leave_page_button_div");
    leave_page_button_div.style.display = "inline";
}

COUNTER = 0;
NUM_CALIBRATIONS = 0;
var BUTTON_POSITIONS = [
    ["0px", "-100px"],
    ["1050px", "-100px"],
    ["1050px", "-600px"],
    ["400px", "-600px"],
    ["700px", "-400px"]
];

function increaseCounter(){
    COUNTER++;
    if(COUNTER == 5){
        COUNTER = 0;
        NUM_CALIBRATIONS++;
        if(NUM_CALIBRATIONS == 5){
            showFile(PATH);
        }
        else {
            moveButtonDivToPosition(NUM_CALIBRATIONS);
        }
    }
}
function moveButtonDivToPosition(idx){
    button_div = document.getElementById("button_div");
    button_div.style.left = BUTTON_POSITIONS[idx][0];
    button_div.style.top = BUTTON_POSITIONS[idx][1];
}
function showButton(){
    button_div = document.getElementById("button_div");
    button_div.style.display = "inline";

    button = document.getElementById("button");
    //button.innerHTML = "Click Me 5 timees";
}


function sendData(value){
    var form = document.myForm;
    form.querySelector("#elapsedInput").value = value/1000;
    form.submit();
}


CURRENT_COLOUR = "white";
function changeBackgroundColour(colour){
    if(CURRENT_COLOUR == colour){
        return;
    }
    document.body.style.backgroundColor = colour;
    CURRENT_COLOUR = colour;
}
function showRedirectionMessage(time){
    message_para = document.getElementById("redirection_message");
    message_para.innerHTML = "Redirecting in " + (5-(time/1000).toFixed(3));
    message_para.style.display = "inline";
    message_para.style.position = "relative";
    message_para.style.left = "0px";
    message_para.style.top = "-50px";

}
function hideRedirectionMessage(){
    message_para = document.getElementById("redirection_message");
    message_para.style.display = "none";
}
function changeDotColour(){
    dot = document.getElementById("webgazerGazeDot");
    dot.style.background = "purple";
}

function eye(){
    num_nulls = 0;
    prev_null_time = -1;
    DATA_SENT = false;

    last_looked_at_document = -1;
    webgazer.setGazeListener(function(data, elapsedTime) {
        if(FIRST_BUTTON_SHOWN == false && webgazer.isReady() && elapsedTime > MIN_TIME){
            FIRST_BUTTON_SHOWN = true;
            showButton();
            changeDotColour();
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

            if(num_nulls >= 6 && STARTED_READING == true){
                console.log("No user");
                if(STARTED_READING && !DATA_SENT){
                    LAST_ELAPSED_TIME = elapsedTime;
                    leave_page();
                }
                nums_nulls = 0;
            }
        }
        else {
            //console.log(elapsedTime);
            if(data.x < 500 && STARTED_READING){
                changeBackgroundColour("red");
                time_looking_away = elapsedTime - last_looked_at_document;
                if(last_looked_at_document != -1){
                    showRedirectionMessage(time_looking_away);
                }
                if(last_looked_at_document != -1 && time_looking_away > 5000 && !DATA_SENT){
                    leave_page();
                }
            }
            else {
                changeBackgroundColour("white");
                last_looked_at_document = elapsedTime;
                hideRedirectionMessage();
            }
        }
        LAST_ELAPSED_TIME = elapsedTime;
    }).begin().showPredictionPoints(true);
}

function leave_page(){
    DATA_SENT = true;
    sendData(LAST_ELAPSED_TIME - BEGIN_TIME);
}
eye();
