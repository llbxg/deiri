// カード情報の取得
function reading(){
    let data = eel.reading()();
    let txt = document.getElementById("number");
    let idm = document.getElementById("idm");
    data.then(function (n) {
        if (n != null ){
            txt.value = n[0];
            idm.value = n[1];
        }
    }).catch(function (error) {
        console.log(error);
        txt.textContent = "Unable to read a card.";
    });
};

// カード情報の登録
function reg(){
    let number = document.getElementById("number");
    let element = document.getElementById("name");
    let idm = document.getElementById("idm");
    if (element != null && number != null){
        let result = eel.reg(idm.value, number.value, element.value)();
        result.then(function (r){
            (async () => {
                if (r){
                    number.value  = "";
                    element.value = "";
                    document.getElementById("display").textContent="Registration was successful.";
                    await sleep(4000);
                }else{
                    document.getElementById("display").textContent="Registration was failed.";
                    await sleep(3000);
                };
            document.getElementById("display").textContent="";
        })();
        });
    };
};