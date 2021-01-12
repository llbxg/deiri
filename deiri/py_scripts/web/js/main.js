// 在室状況の取得 | 表示
function getMembers(){
    let m = document.getElementById('members');
    while (m.firstChild) m.removeChild(m.firstChild);
    let a = eel.room_members()();

    a.then(function (member) {
        console.log(member)
        for (let number in member){
            let c = getCookies(`${number}`);
            let div = document.createElement('div');
            div.className = 'member';
            div.setAttribute('name', number)
            div.setAttribute('onclick','changeIcon(this);');

            let icon;
            let v;
            if (typeof c === 'undefined'){
                setCookie(number, 0)
                icon = 'room'
                v='0'
            } else {
                switch (c[1]) {
                case '0':
                    icon = 'room'
                    v='0'
                    break
                case '1':
                    icon = 'restaurant'
                    v='1'
                    break
                case '2':
                    icon = 'science'
                    v='2'
                    break
                case '3':
                    icon = 'school'
                    v='3'
                    break
                }
            }

            div.setAttribute('value', v)
            div.innerHTML = `<div class='material-icons'>${icon}</div><div class='name'>${member[number].replace('\u3000','')}</div>`;

            m.appendChild(div);
            scrollToTop();
        }
    }).catch(function (error) {
        console.log(error);
    });
};

function getCookies(key){
    let cookies = document.cookie;
    let cookiesArray = cookies.split(';');
    console.log(cookiesArray)

    for(let c of cookiesArray){
        let cArray = c.split('=');
        cArray[0] = cArray[0].replace(/\s+/g, "")
        if( cArray[0] == key){
            return cArray
        }
    }
}

function setCookie(key, value){
    let nowDay = new Date();
    var nextDay = new Date( nowDay.getFullYear(), nowDay.getMonth(), nowDay.getDate()+1);
    nowDay.setTime(nowDay.getTime() + (nextDay - nowDay));
    document.cookie = `${key}=${value}; expires=${nowDay}`;
}

function changeIcon(t){

    let n = t.getAttribute('name');
    let v = t.getAttribute('value');
    let i = t.children[0]

    switch (v) {
    case '0':
        setCookie(n, 1)
        t.setAttribute('value', '1')
        i.textContent = 'restaurant'
        break
    case '1':
        setCookie(n, 2)
        t.setAttribute('value', '2')
        i.textContent = 'science'
        break
    case '2':
        setCookie(n, 3)
        t.setAttribute('value', '3')
        i.textContent = 'school'
        break
    case '3':
        setCookie(n, 0)
        t.setAttribute('value', '0')
        i.textContent = 'room'
        break
    }
}


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