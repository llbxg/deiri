// 在室状況の取得 | 表示
function getMembers(){
    let m = document.getElementById('members');
    while (m.firstChild) m.removeChild(m.firstChild);
    let a = eel.room_members()();

    a.then(function (member) {
        for (let number in member){
            let div = document.createElement('div');
            div.className = 'member';
            div.setAttribute('name', number)
            console.log(member[number]);
            div.textContent = member[number].replace('\u3000','');
            m.appendChild(div);
            scrollToTop();
        }
    }).catch(function (error) {
        console.log(error);
    });
};

// 入退室の際のデータを回収 | 表示
eel.expose(say_hello_or_seeu);
function say_hello_or_seeu(x) {
    if (x!=null){  // if <- 完全に一応って感じの処理
        (async () => {  // displayを一瞬(3.5s)表示する
            let txt = document.getElementById("display");
            txt.textContent = x.replace('\u3000','');  // 全角スペースはダサいので
            getMembers();
            scrollToTop();
            await sleep(3500);
            txt.textContent = "";
        })();
    };
};

function scrollToTop() {
    scrollTo(0, 0);
}