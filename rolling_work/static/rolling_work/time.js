document.addEventListener('DOMContentLoaded', function() {
    init();
    document.querySelector('#start').addEventListener('click', start_time);
    document.querySelector('#roll').addEventListener('click', roll);
    document.querySelector('#pause').addEventListener('click', stop_start);
});
var state, last_sec, now_sec;
var is_paused = false;
var sec, min, hr;
function init() {
    document.querySelector('#start').style.display = 'block';
    document.querySelector('#roll').style.display = 'none';
    document.querySelector('#pause').style.display = 'none';
    document.querySelector('#save').style.display = 'none';

    document.querySelector('#snowman').style.display = "none";
    document.querySelector('#space').style.display = "block";

    state = "Work";
    last_sec = 0; now_sec = 0;
    sec = 0, min = 0, hr = 0;
}
function add_zero(num) {
    if (num < 10) {
        return '0'+num.toString();
    }
    return num.toString();
}
function start_time() {
    document.querySelector('#start').style.display = 'none';
    document.querySelector('#roll').style.display = 'block';
    document.querySelector('#pause').style.display = 'block';
    document.querySelector('#save').style.display = 'block';
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
function roll() {
    record = document.querySelector('#record-area');

    new_record = document.createElement('div');
    new_record.classList.add('record-card');
    // new_record.classList.add('glow');
    
    let sec_passed = now_sec - last_sec;
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