'use strict';

const HOST = 'http://127.0.0.1:8080'


chrome.extension.onMessage.addListener(function(request, sender, sendResponse) {
	if (request == "Action") {
		see_pekora();
	}
});

//
function see_pekora() {

    // A greeting from Pekora
    alert("こんぺこ！こんぺこ！こんぺこー！ホロライブ3期生の兎田ぺこらぺこ～！");

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
        error => alert('だめぺこ')
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
