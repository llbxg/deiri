// 長時間の放置は自動的にホームへ遷移させます。

async function wait(t=60){
    await sleep(t*1000);
    window.location.href="/html/contents/main.html";
};