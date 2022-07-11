document.addEventListener('DOMContentLoaded', function() {
    init();
    update_time();
    if (document.querySelector('#start') !== null) {
        document.querySelector('#start').addEventListener('click', start_time);
    }
    if (document.querySelector('#roll') !== null) {
        document.querySelector('#roll').addEventListener('click', () => roll_func(true));
    }
    if (document.querySelector('#pause') !== null) {
        document.querySelector('#pause').addEventListener('click', stop_start);
    }
    
    if (document.querySelector('#save') !== null) {
        document.querySelector('#save').addEventListener('click', save_record);
    }
    // window.onload = updateCheck;
});
var state, last_sec, now_sec;
var is_paused = false;
var sec, min, hr;

// model variables
var LWP, LRP, WT, AT, RC;
var SWP, SRP;

function init() {
    if (document.querySelector('#start') !== null) {
        document.querySelector('#start').style.display = 'block';
    }
    if (document.querySelector('#roll') !== null) {
        document.querySelector('#roll').style.display = 'none';
    }
    if (document.querySelector('#pause') !== null) {
        document.querySelector('#pause').style.display = 'none';
    }
    if (document.querySelector('#save') !== null) {
        document.querySelector('#save').style.display = 'none';
    }

    if (document.querySelector('#snowman') !== null) {
        document.querySelector('#snowman').style.display = "none";
    }
    if (document.querySelector('#space') !== null) {
        document.querySelector('#space').style.display = "block";
    }
    
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
function roll_func(ctl) {
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
    if (ctl) { // from click not from pause
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
    }

    record.prepend(new_record);
}
function stop_start() {
    console.log("stop start", state, is_paused);
    if (state === "Work" && !is_paused) {
        roll_func(false);
    }
    pause_btn = document.querySelector('#pause');
    console.log(pause_btn.innerHTML);
    if (is_paused) { // continue
        console.log('A');
        is_paused = false;
        pause_btn.innerHTML = "Pause";
        document.querySelector('#roll').style.display = 'block';
        // if (document.querySelector('#save') !== null) {
        //     document.querySelector('#save').style.display = 'none';
        // }
    }
    else {
        console.log('B');
        is_paused = true;
        pause_btn.innerHTML = "Resume";
        document.querySelector('#roll').style.display = 'none';
        // if (document.querySelector('#save') !== null) {
        //     document.querySelector('#save').style.display = 'block';
        // }
    }
}
// var LWP, LRP, WT, AT, RC;
// var SWP, SRP;
function save_record() {
    roll_func();
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
        // console.log(data["record_id"]);
        location.href = `/record/${data["record_id"]}`;
    });    
}

function update_time() {
    document.querySelectorAll('.record-time').forEach(clock => {
        let time = clock.innerHTML;
        
        const hour_regex = /[0-9]+:/g;
        const hour_idx = time.search(hour_regex);
        const hour_str = time.slice(hour_idx, hour_idx+2);
        let hour = Number(hour_str);
        
        const date_regex = /[0-9]+,/g;
        const date_idx = time.search(date_regex);
        const date_str = time.slice(date_idx, date_idx+2);
        let date = Number(date_str);

        // console.log(hour, date);

        const d = new Date();
        let diff = d.getTimezoneOffset() / (-60);
        hour += diff;
        if (hour >= 24) {
            hour %= 24;
            date += 1;
            time = time.replace(date_str, add_zero(date));
        }
        else if (hour < 0) {
            hour += 24;
            date -= 1;
            time = time.replace(date_str, add_zero(date));
        }
        time = time.replace(hour_str, add_zero(hour));
        clock.innerHTML = time;
    });
}