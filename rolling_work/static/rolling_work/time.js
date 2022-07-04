document.addEventListener('DOMContentLoaded', function() {
    init();
    document.querySelector('#start').addEventListener('click', start_time);
});

function init() {
    document.querySelector('#start').style.display = 'block';
    document.querySelector('#roll').style.display = 'none';
    document.querySelector('#pause').style.display = 'none';
    document.querySelector('#save').style.display = 'none';
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
    let sec = 0, min = 0, hr = 0;
    setInterval(() => {
        sec += 1;
        if (sec > 60) {
            sec %= 60; min += 1;
        }
        if (min > 60) {
            min %= 60; hr += 1;
        }
        document.querySelector('#cur_time').innerHTML = `${add_zero(hr)}:${add_zero(min)}:${add_zero(sec)}`;
        console.log('plus one');
    }, 1000);
    
}