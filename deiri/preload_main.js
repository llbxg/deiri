const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld(
    "api", {
        close: () => {
            ipcRenderer.send('close', "");
        },
    }
);

const flatpickr = require("flatpickr");
contextBridge.exposeInMainWorld(
    "flatpickr", {
        flatpickr: (element, w) =>{
            flatpickr(element, {
                enableTime: true,
                dateFormat: "Y-m-d H:i",
                onChange: function(selectedDates, dateStr){
                    let e;
                    if(w==0){
                        e = document.getElementById('start');
                    } else {
                        e = document.getElementById('finish');
                    }
                    e.value = dateStr
                }
                }
            );
        }
    }
);