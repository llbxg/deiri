function calendar(y, m){
    const date1 = new Date();
    const weeks = ['日', '月', '火', '水', '木', '金', '土']
    const year = y
    const month = m
    const startDate = new Date(year, month, 1)
    const endDate = new Date(year, month,  0)
    const endDayCount = endDate.getDate()
    const startDay = startDate.getDay()
    let dayCount = 1
    let calendarHtml = ''

    let when = document.getElementById('when')
    when.innerHTML = `<div id='year'>${year}</div>/<div id='month'>${month}</div>`

    calendarHtml += '<table>'

    calendarHtml += '<tr>'
    for (let i = 0; i < weeks.length; i++) {
        calendarHtml += '<td>' + weeks[i] + '</td>'
    }
    calendarHtml += '</tr>'

    for (let w = 0; w < 6; w++) {
        calendarHtml += '<tr>'

        for (let d = 0; d < 7; d++) {
            if (w == 0 && d < startDay) {
                calendarHtml += '<td></td>'
            } else if (dayCount > endDayCount) {
                calendarHtml += '<td></td>'
            } else {
                console.log(date1.getFullYear()==year&& date1.getMonth()+1==month&& date1.getDate()==dayCount);
                if(date1.getFullYear()==year && date1.getMonth()+1==month && date1.getDate()==dayCount){
                    calendarHtml += `<td id='today' onclick="func(${year}, ${month}, ${dayCount});">${dayCount}</td>`
                }else{
                    calendarHtml += `<td onclick="func(${year}, ${month}, ${dayCount});">${dayCount}</td>`
                }

                dayCount++
            }
        }
        calendarHtml += '</tr>'
    }
    calendarHtml += '</table>'

    document.querySelector('#calendar').innerHTML = calendarHtml
}

const date = new Date();
let yy = date.getFullYear();
let mm = date.getMonth()+1;
let dd = date.getDate();
document.getElementById('when').textContent = `${mm}/${dd}`
window.onload = func(yy, mm, dd)
calendar(yy, mm);



function func(y, m, d){
    let scheduleHtml = ''
    scheduleHtml+=`<div id='date'> <div id='y'>${y}</div>/<div id='m'>${m}</div>/<div id='d'>${d}</div></div> `
    document.querySelector('#schedule').innerHTML = scheduleHtml
    let l= document.getElementById('list');
    l.innerHTML = ''
    let a = eel.getdate(y, m, d)();
        a.then(function (list) {
            for (let number in list){
                console.log();(list[number])
                const label = document.createElement('label');
                const span = document.createElement('span');
                const input = document.createElement('input');
                input.setAttribute("type","radio");
                input.setAttribute("name","radio");
                input.className = 'radioinput';
                input.setAttribute("value",list[number][0]);
                label.className = 'radio-btn';
                span.className = 'radio-txt';

                span.textContent = ` ${number} | ${list[number][0][2]} ${list[number][0][3]}:${list[number][0][4]} ~ ${list[number][1][2]} ${list[number][1][3]}:${list[number][1][4]} ${list[number][2]}`;
                label.appendChild(input);
                label.appendChild(span);
                l.appendChild(label);
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
            console.log(err);
        });
}

const prev = document.getElementById("prev");
prev.addEventListener("click", function() {
    button(-1)
});

const next = document.getElementById("next");
next.addEventListener("click", function() {
    button(1)
});

function button(c){
    let y = parseInt(document.getElementById('year').textContent);
    let m = parseInt(document.getElementById('month').textContent);
    if(m==1 && c == -1){
        m = 12;
        y -= 1;
    } else {if (m==12 && c == 1){
        m = 1;
        y += 1;
    } else {
        m += c
    }};
    console.log();(y, m);
    calendar(y, m);
}

function getMembers(){
    let m = document.getElementById('schedules');
    while (m.firstChild) m.removeChild(m.firstChild);
    let a = eel.timedate()();

    a.then(function (member) {
        console.log(member)
        for (let number in member){
            let div = document.createElement('div');
            div.className = 'member';
            div.setAttribute('name', number)
            console.log(member[number]);
            div.textContent = member[number].replace('\u3000','');
            m.appendChild(div);
        }
    }).catch(function (err) {
        console.log();("somthing went to wrong", err)
    });
};

function getAllMember(){
    let mem = document.getElementById('memberList');
    let o = eel.check_all_users()();
    o.then(function (member) {
        console.log(member)
        for (let number in member){
            const option = document.createElement('option');
            option.setAttribute("value",`${number},${member[number]}`);
            option.textContent = `${number} | ${member[number]}`;
            mem.appendChild(option);
        };
    }).catch(function (err) {
        console.log();("somthing went to wrong", err)
    });
};

getAllMember()

const fpStart = window.flatpickr.flatpickr('#calendarStart',0);
const fpFinish = window.flatpickr.flatpickr('#calendarFinish',1);



function send(){
    let dateStrStart = document.getElementById('start').value;
    let dateStrFinish = document.getElementById('finish').value;
    let data = document.getElementById('memberList').value;
    if (data!=""){
        data = data.split(',');
        const number = data[0];
        eel.res(dateStrStart, dateStrFinish, number)();
    };
}

eel.expose(nok);
function nok(x) {
    if (x!=null){
        (async () => {
            let txt = document.getElementById("display");
            txt.textContent = x;
            await sleep(3500);
            txt.textContent = "";
        })();
    }
}

eel.expose(clean);
function clean() {
    let y = parseInt(document.getElementById('y').textContent);
    let m = parseInt(document.getElementById('m').textContent);
    let d = parseInt(document.getElementById('d').textContent);
    func(y, m, d);
    let data = document.getElementById('memberList');
    data.value = '';
}