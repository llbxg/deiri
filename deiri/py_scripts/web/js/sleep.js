// async/awaitを使ったスリープの定義しておきます。

const sleep = msec => new Promise(resolve => setTimeout(resolve, msec));