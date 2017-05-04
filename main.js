let pyProc = null
let pyPort = null

const selectPort = () => {
    pyPort = 4242
    return pyPort
}

const createPyProc = () => {
    let port = '' + selectPort()
    let script = path.join(__dirname, 'jsonrpc', 'jsonrpc.py')
    console.log(script)
    pyProc = require('child_process').spawn('python', [script])
    if (pyProc != null) {
        console.log('child process success')
        //console.log(pyProc)
        pyProc.stdout.on('data', function (data) {

        });
    }

}


const exitPyProc = () => {
    pyProc.kill()
    pyProc = null
}

fs = require("fs")
d3 = require("d3")
const {
    app,
    BrowserWindow,
    Menu,
    dialog,
    ipcMain
} = require('electron')

app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)
const path = require('path')
const url = require('url')

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win
let dispatch = d3.dispatch("open", "about")
let showOpen = function () {
    dialog.showOpenDialog({
        properties: ['openFile'],
        filters: [{
            extensions: ['txt']
        }]
    }, function (d) {
        console.log(d)
        dispatch.call("open", this, d)
    })
};

function createWindow() {
    // Create the browser window.
    win = new BrowserWindow({
        width: 900,
        height: 800
    })
    const menuTemplate = [{
        label: 'BranchPoint',
        submenu: [{
            label: 'About ...',
            click: () => {
                console.log('About Clicked');
                dispatch.call("about", this, {})

                dialog.showMessageBox({
                    message: 'BranchPoint Version v0.1 powered by Electron',
                    buttons: []
                });
            }

        }, {
            type: 'separator'
        }, {
            label: 'Quit',
            click: () => {
                app.quit();
            }
        }]
    }, {
        label: 'File',
        submenu: [{
            label: "Open",
            click: () => {
                showOpen()
            }
        }]
    }];
    const menu = Menu.buildFromTemplate(menuTemplate);
    Menu.setApplicationMenu(menu);
    // and load the index.html of the app.
    win.loadURL(path.join("file://", __dirname, "index.html"))

    // Open the DevTools.
    // win.webContents.openDevTools()

    // Emitted when the window is closed.
    win.on('closed', () => {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        console.log("close main window")
        win = null
        app.quit()
    })
    dispatch.on("open", function (d) {
        win.webContents.send('info', {
            "code": "files",
            "files": d
        })
    })
    dispatch.on("about", function (d) {
        win.webContents.send('info', {
            "code": "about"
        })
    })

}
// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit()
    }

})

app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (win === null) {
        createWindow()
    }
})
