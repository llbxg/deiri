// 所属Userの取得 | <form id="list">に追加
function getAllMember(){
    let m= document.getElementById('list');
    let o = eel.check_all_users()();
    o.then(function (member) {
        for (let number in member){
            console.log(member[number])
            const label = document.createElement('label');
            const span = document.createElement('span');
            const input = document.createElement('input');
            input.setAttribute("type","radio");
            input.setAttribute("name","radio");
            input.className = 'radioinput';
            input.setAttribute("value",number);
            label.className = 'radio-btn';
            span.className = 'radio-txt';
            span.textContent = ` ${number} | ${member[number].replace('\u3000','')}`;
            label.appendChild(input);
            label.appendChild(span);
            m.appendChild(label);
        };
        let radioLabel = document.getElementsByClassName('radio-btn');
        for (let i = 0; i < radioLabel.length; i++){
            radioLabel[i].addEventListener('click', function(event){
                event.preventDefault();
                let inputEl = this.querySelector('input');
                inputEl.checked = !inputEl.checked;
            });
            }
    }).catch(function (error) {
        console.log(error);
    });
};

// User情報の削除
function del (){
    const element = document.getElementById( "list" ) ;
    const  radioNodeList = element.radio ;
    const number = radioNodeList.value;
    if ( number !== "" ) {
        // confirmの内容にlocalhost:portって出るの嫌なので、そのうちモーダル不可避。
        const result = confirm(`学生証番号[ ${number} ]を消去します。`);
        if (result){
            const comm = document.getElementById('display');
            let r = eel.delete(number)();
            r.then((b)=>{
                (async () => {
                    console.log(b)
                    if(b){
                        let m= document.getElementById('list');
                        m.textContent = null;
                        getAllMember();
                        comm.textContent = "Successful"
                        await sleep(1*4000);
                    }else{
                        comm.textContent = "Failed"
                        await sleep(1*4000);
                    }
                    comm.textContent = ""

                })();

            }, err=>{
                console.log("somthing went to wrong", err)
            })

        }
    }
};