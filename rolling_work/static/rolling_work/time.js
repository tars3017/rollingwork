document.addEventListener('DOMContentLoaded', function() {
    console.log('line 2');
    init();
    document.querySelector('#start').addEventListener('click', start_time);
    document.querySelector('#roll').addEventListener('click', roll_func);
    document.querySelector('#pause').addEventListener('click', stop_start);
    if (document.querySelector('#save') !== null) {
        document.querySelector('#save').addEventListener('click', save_record);
    }
    window.onload = updateCheck();
});
var state, last_sec, now_sec;
var is_paused = false;
var sec, min, hr;

// model variables
var LWP, LRP, WT, AT, RC;
var SWP, SRP;

function init() {
    document.querySelector('#start').style.display = 'block';
    document.querySelector('#roll').style.display = 'none';
    document.querySelector('#pause').style.display = 'none';
    if (document.querySelector('#save') !== null) {
        document.querySelector('#save').style.display = 'none';
    }

    document.querySelector('#snowman').style.display = "none";
    document.querySelector('#space').style.display = "block";

    state = "Work";
    last_sec = 0; now_sec = 0;
    sec = 0, min = 0, hr = 0;

    LWP = 0, LRP = 0, WT = 0, AT = 0, RC = 0;
    SWP = 86400, SRP = 86400;
}
function add_zero(num) {
    if (num < 10) {
        return '0'+num.toString();
    }
    return num.toString();
}
function start_time() {
    init();
    document.querySelector('#start').style.display = 'none';
    document.querySelector('#roll').style.display = 'block';
    document.querySelector('#pause').style.display = 'block';
    if (document.querySelector('#save') !== null) {
        document.querySelector('#save').style.display = 'block';
    }
        setInterval(() => {
            if (!is_paused) {
                sec += 1;
                now_sec += 1;
                if (sec >= 60) {
                    sec %= 60; min += 1;
                }
                if (min >= 60) {
                    min %= 60; hr += 1;
                }
                document.querySelector('#cur_time').innerHTML = `${add_zero(hr)}:${add_zero(min)}:${add_zero(sec)}`;
            }
        }, 1000);
}
function roll_func() {
    record = document.querySelector('#record-area');

    new_record = document.createElement('div');
    new_record.classList.add('record-card');
    // new_record.classList.add('glow');
    
    let sec_passed = now_sec - last_sec;
    RC += 1;
    if (state == "Work") {
        LWP = Math.max(LWP, sec_passed);
        SWP = Math.min(SWP, sec_passed);
        WT += sec_passed;
    }
    else {
        LRP = Math.max(LRP, sec_passed);
        SRP = Math.min(SRP, sec_passed);
    }
    last_sec = now_sec;
    let min_passed = Math.floor(sec_passed / 60);
    sec_passed %= 60;
    let hr_passed = Math.floor(min_passed / 60);
    min_passed %= 60;

    console.log(state);
    new_record.innerHTML = `${state} ${add_zero(hr_passed)}:${add_zero(min_passed)}:${add_zero(sec_passed)}`;
    if (state === "Work") {
        state = "Rest";
        document.querySelector('#snowman').style.display = "block";
        document.querySelector('#space').style.display = "none";
    }
    else {
        state = "Work";
        document.querySelector('#snowman').style.display = "none";
        document.querySelector('#space').style.display = "block";
    }

    record.prepend(new_record);
}
function stop_start() {
    pause_btn = document.querySelector('#pause');
    console.log(pause_btn.innerHTML);
    if (is_paused) { // continue
        console.log('A');
        is_paused = false;
        pause_btn.innerHTML = "Pause";
        document.querySelector('#roll').style.display = 'block';
    }
    else {
        console.log('B');
        is_paused = true;
        pause_btn.innerHTML = "Resume";
        document.querySelector('#roll').style.display = 'none';
    }
}
// var LWP, LRP, WT, AT, RC;
// var SWP, SRP;
function save_record() {
    stop_start();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(csrftoken);
    console.log('save');
    AT = hr*3600 + min*60 + sec;

    const request = new Request(
        '/save',
        {headers: {'X-CSRFToken': csrftoken}}
    );
    fetch(request, {
        method: 'POST',

        body: JSON.stringify({
            nLWP: LWP,
            nLRP: LRP,
            nWT: WT,
            nAT: AT,
            nRC: RC,
            nSWP: SWP,
            nSRP: SRP
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data["record_id"]);
        location.href = `/record/${data["record_id"]}`;
    });    
}