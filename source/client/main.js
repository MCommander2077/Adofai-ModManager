const path = require('path')
const { app, BrowserWindow } = require('electron');
function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600
  })

  win.loadURL('https://music.163.com/')
}

app.whenReady().then(() => {
  createWindow()
})

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})