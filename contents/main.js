'use strict';

const HOST = 'http://127.0.0.1:8080'

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

    const action = request.action;
    const flag = request.flag;
    let response = [];

    console.log("Arrive in content.js for " + action);

    addStylesheet();

    switch (action) {
        case "translation":
            readPekora(); break;
        case "cursor":
            usePekora(flag); break;
        case "images":
            seePekora(); break;
        case "almond":
            response = getAlmondStatus(); break;
        default:
            ;
    }

    sendResponse(response);
    return true;
});

//
const readPekora = () => {
    // A greeting from Pekora
    console.log("こんぺこ！こんぺこ！こんぺこー！ホロライブ3期生の兎田ぺこらぺこ～！");

    // Display the loading gif
    import("./modules/loading.js").then( module => module.displayLoading() );
    // Translate
    import("./modules/translation.js").then( module => module.translate() );
}

const usePekora = (flag) => {
    import("./modules/loading.js").then( module => module.displayLoading() );
    import("./modules/cursor.js").then( module => {
            (flag) ? module.usePekora_cursor() : module.remove_pekora_cursor();
        })
}

const seePekora = () => {
    import("./modules/loading.js").then( module => module.displayLoading() );
    import("./modules/switch.js").then( module => module.switch_imgs() );
}

// 機能の使用状況を把握
const getAlmondStatus = () => {
    const almond_status = [false, true, true];
    console.log("Check almond status");
    return almond_status;
}

const addStylesheet = () => {

    // 既に追加済みの場合は戻る;
    if (document.getElementById("loading-css") !== null) { return };

    const link_tag = document.createElement('link');
    link_tag.rel = "stylesheet";
    link_tag.href = chrome.extension.getURL("contents/css/loading.css");
    link_tag.id = "loading-css";

    document.getElementsByTagName('head')[0].appendChild(link_tag);
}
