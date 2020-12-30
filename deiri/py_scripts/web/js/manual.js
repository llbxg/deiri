// 所属メンバーの取得 | <select>に追加
function getAllMember(){
    let m = document.getElementById('memberList');
    let o = eel.check_all_users()();
    o.then(function (member) {
        console.log(member)
        for (let number in member){
            const option = document.createElement('option');
            option.setAttribute("value",`${number},${member[number]}`);
            option.textContent = `${number} | ${member[number]}`;
            m.appendChild(option);
        };
        let radioLabel = document.getElementsByClassName('radio-btn');
        for (let i = 0; i < radioLabel.length; i++){
            radioLabel[i].addEventListener('click', function(event){
                event.preventDefault();
                let inputEl = this.querySelector('input');
                inputEl.checked = !inputEl.checked;
            });
            };
    }).catch(function (error) {
        console.log(error);
    });
};

// 在室状況の取得 | 表示
function deiri(){
    let data = document.getElementById('memberList').value;
    if (data!=""){
        data = data.split(',');
        const number = data[0];
        const name = data[1];
        eel.instant_deiri(name, number);
    };
}

// /main.py/ 入退室の際のデータを回収
eel.expose(say_hello_or_seeu2);
function say_hello_or_seeu2(x) {
    if (x!=null){  // if <- 完全に一応って感じの処理
        (async () => {  // displayを一瞬(3.5s)表示する
            let txt = document.getElementById("display");
            txt.textContent = x.replace('\u3000','');  // 全角スペースはダサいので
            await sleep(3500);
            txt.textContent = "";
        })();
    }
}