function closeAd(){
    const boxes = document.getElementsByName("ad");
    const cnt = boxes.length;
    for(let i=0; i<cnt; i++) {
        if(boxes.item(i).checked) {
            boxes.item(i).checked = false;
        }
    }
}

function countAdClick(n){
    const boxes = document.getElementById(`acd-check${n}`);
    if(boxes.checked){
        eel.count_checkbox(n)
    }
}