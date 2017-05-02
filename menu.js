const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const Menu = electron.Menu;
const {dialog} = require('electron');
var showOpen = function() {
		dialog.showOpenDialog({ properties: [ 'openFile'], filters: [{ extensions: ['txt'] }]},function(d){console.log(d)});
};


app.on('ready', function () {
   new BrowserWindow();
    const menuTemplate = [
        {
            label: 'Electron',
	    submenu: [
            {
                label: 'About ...',
                click: () => {
                    console.log('About Clicked');
                }

            },{
		type: 'separator'
	    },{
                label: 'Quit',
                click: () => {
                    app.quit();
                }
            }
           ]
        }, {
		label:'File',
		submenu: [
		{
			label:"Open",
			click: () => { showOpen() }
		}
		]
	}
    ];
    const menu = Menu.buildFromTemplate(menuTemplate);
    Menu.setApplicationMenu(menu);
});
