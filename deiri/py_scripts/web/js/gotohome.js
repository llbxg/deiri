// 長時間の放置は自動的にホームへ遷移させます。

async function wait(){
    await sleep(60*1000);
    window.location.href="/html/contents/main.html";
};