'use strict';

const HOST = 'http://127.0.0.1:8080'

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {

    const action = request.action
    const flag = request.flag
    let response = [];

    console.log("Arrive in content.js for " + action);

    switch (action) {
        case "translation":
            see_pekora();
            break;

        case "cursor":
            (flag) ? use_pekora_cursor() : remove_pekora_cursor();
            break;

        case "images":
            switch_imgs();
            break;

        case "almond":
            response = get_almond_status();
            break;

        default:
            ;
    }

    sendResponse(response);
    console.log("Response sent");

    return true;
});


const use_pekora_cursor = () => {
    const arrowUrl = chrome.extension.getURL("../images/cursors/pekora_arrow.png");
    const pointerUrl = chrome.extension.getURL("../images/cursors/carrot_pointer.png");

    // 通常カーソル
    $("body").css("cursor", "URL('" + arrowUrl + "'), auto");

    // なんとかhover時カーソル
    const pointer_tag = ["a", "button", "label a"];
    pointer_tag.map( tag => $(tag).css("cursor", "URL('" + pointerUrl + "'), pointer") );

    console.log("Activate Pekora cursor");
}

const remove_pekora_cursor = () => {
    $("body").css("cursor", "auto");
    console.log("Deactivate Pekora cursor");
}

const switch_imgs = () => {
    console.log("Switch images")
}

// 機能の使用状況を把握
const get_almond_status = () => {
    const almond_status = [false, true, true]
    console.log("Check almond status")
    return almond_status
}

//
function see_pekora() {
    // A greeting from Pekora
    console.log("こんぺこ！こんぺこ！こんぺこー！ホロライブ3期生の兎田ぺこらぺこ～！");

    // Scrape body & headlines and create dictionary
    const sentence_dict = scrape()

    // Send the dict to views.py
    send_to_py(sentence_dict);
}


function scrape() {
    const tag_array = ['p', 'li', 'th', 'td', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        .filter((tag) => (document.getElementsByTagName(tag).length != 0));

    const body_tag = ['p'];
    const sentence_dict = {'body': {}, 'headline': {}};

    tag_array.forEach(function(tag) {
        if ( body_tag.includes(tag) ) {
            sentence_dict['body'][tag] = [].concat(
                Array.from(document.getElementsByTagName(tag)).map(item => item.innerHTML));
        } else {
            sentence_dict['headline'][tag] = [].concat(
                Array.from(document.getElementsByTagName(tag)).map(item => item.innerHTML));
        }
    })
    return sentence_dict
}

// Ajax
function send_to_py(array) {

    const data_to_python = JSON.stringify(array);
    $.ajax({
      type          : 'POST',
      url           : HOST + '/pekora',
      data          : data_to_python,
      contentType   : 'application/json'

    })
    .then(
        // Success
        data => {
            const result = JSON.parse(data);
            replace_all(result.body);
            replace_all(result.headline)
        },
        // Failure
        error => alert('翻訳失敗ぺこ！！')
    );

}

function replace_all(dict) {
    const tags = Object.keys(dict)
    tags.forEach(function(tag) {
        const originals = document.getElementsByTagName(tag);
        const pekos = dict[tag];
        for (let i = 0; i < originals.length; i++) {
            originals[i].innerHTML = pekos[i];
        }
    })
}
