// 時間を表示する

function tim(){
    const date = new Date();
    const strTime = ' '
            + ('0' + (date.getMonth()+1)).slice(-2) + '/'
            + ('0' + date.getDate()).slice(-2) + ' '
            + `(${[ "日", "月", "火", "水", "木", "金", "土" ][date.getDay()]}) `
            + ('0' + date.getHours()).slice(-2)
            + ':' + ('0' + date.getMinutes()).slice(-2)
            + ':' + ('0' + date.getSeconds()).slice(-2);

    if (date.getHours()==1 && date.getMinutes()==45 && date.getSeconds()==1){
        window.location.href="/html/contents/main.html";
    }

    return strTime
};

const m = document.getElementById('time');
m.textContent = tim();
const intervalId = setInterval(()=>{
    m.textContent = tim();
}, 1*1000);