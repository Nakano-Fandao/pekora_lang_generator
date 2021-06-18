'use strict';

const HOST = 'http://127.0.0.1:8080'

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

    const action = request.action
    const flag = request.flag
    let response = [];

    console.log("Arrive in content.js for " + action);

    switch (action) {
        case "translation":
            read_pekora(); break;
        case "cursor":
            use_pekora(flag); break;
        case "images":
            see_pekora(); break;
        case "almond":
            response = get_almond_status(); break;
        default:
            ;
    }
    sendResponse(response);
    console.log("Response sent");
    return true;
});

//
const read_pekora = () => {
    // A greeting from Pekora
    console.log("こんぺこ！こんぺこ！こんぺこー！ホロライブ3期生の兎田ぺこらぺこ～！");

    // Display the loading gif


    // Translate
    import("./modules/translation.js")
        .then( module => module.translate() )
}

const use_pekora = (flag) => {
    import("./modules/cursor.js")
        .then( module => {
            (flag) ? module.use_pekora_cursor() : module.remove_pekora_cursor();
        })
}

const see_pekora = () => {
    import("./modules/switch.js")
        .then( module => module.switch_imgs() )
}

// 機能の使用状況を把握
const get_almond_status = () => {
    const almond_status = [false, true, true]
    console.log("Check almond status")
    return almond_status
}

const display_loading = () => {
    //

    const h = window.innerHeight;

}
