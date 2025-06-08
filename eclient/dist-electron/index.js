"use strict";
const electron = require("electron");
const path = require("path");
const createWindow = () => {
  const win = new electron.BrowserWindow({
    webPreferences: {
      contextIsolation: false,
      // 是否开启隔离上下文
      nodeIntegration: true,
      // 渲染进程使用Node API
      preload: path.join(__dirname, "./preload.js")
      // 需要引用js文件
    }
  });
  if (process.env.NODE_ENV !== "development") {
    win.loadFile(path.join(__dirname, "./index.html"));
    win.webContents.openDevTools();
  } else {
    let url = "http://localhost:5173";
    win.loadURL(url);
    win.webContents.openDevTools();
  }
};
electron.app.whenReady().then(() => {
  createWindow();
  electron.app.on("activate", () => {
    if (electron.BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});
electron.app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    electron.app.quit();
  }
});
