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

export {use_pekora_cursor, remove_pekora_cursor};
