const { app, BrowserWindow, ipcMain } = require('electron');
const {PythonShell} = require('python-shell');
const path = require('path');
const execSync = require('child_process').execSync;
let win = null

function createWindow () {
    win = new BrowserWindow({
        minWidth: 800,
        minHeight: 450,
        'fullscreen': true,
        frame: false,
        backgroundColor:'white',
        icon: 'build/icon.png',

        webPreferences: {
            worldSafeExecuteJavaScript: true,
            nodeIntegration: false,
            contextIsolation: true,
            preload: __dirname + '/preload_main.js'
        },
    })

    win.setMenu(null);

    win.loadFile(path.join(__dirname, 'py_scripts/web/index.html'))

    win.webContents.openDevTools()

    win.once('ready-to-show', () => {
        win.show()
    })

    win.on('closed', () => {
        win = null
    })
};


app.whenReady().then(() => {
    const script =  process.env.DEIRI_SCRIPT==null ? path.join(__dirname, '../app.asar.unpacked/py_scripts') : process.env.DEIRI_SCRIPT
    const python =  execSync('which python').toString().replace(/\r?\n/g,"");

    let options = {
        pythonPath: python,
        scriptPath: script,
        args: [app.getPath('home')]
    };

    PythonShell.run('/main.py', options, function (err, result) {
    if (err) throw err;
        console.log(result);
    });

    console.log(app.getPath('home'))

    createWindow()
});

const doubleboot = app.requestSingleInstanceLock();
if(!doubleboot){
    app.quit();
}

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
});

ipcMain.on("close", (event, args) => {
    win.close()
});