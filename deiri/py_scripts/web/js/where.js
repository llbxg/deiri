const locate = window.location.href.split('/').pop().split('.').shift();
console.log(`locate : ${locate}`);
eel.where_am_i(locate)();  // 位置情報の送信