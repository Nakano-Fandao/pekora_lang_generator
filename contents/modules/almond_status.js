// 機能の使用状況を把握
const checkAlmondStatus = () => {

    // 既に追加済みの場合は戻る;
    const almond_tag = createAlmondTag();

    const almond_status = [];
    const action_list = ["translation", "cursor", "images"];
    action_list.map( action => {
        almond_status.push(almond_tag.classList.contains(action))
    });
    return almond_status;
}

const updateAlmondStatus = (action, flag) => {

    // 既に追加済みの場合は戻る;
    const almond_tag = createAlmondTag();

    // アクションに応じて、classにaction名を追加する
    switch (flag) {
        case true:
            almond_tag.classList.add(action); break;
        case false:
            almond_tag.classList.remove(action); break;
        default:
            ;
    }

}

// なければ作成
const createAlmondTag = () => {

    // 既に追加済みの場合は戻る;
    if (document.getElementById('almond-status') === null) {
        const new_almond_tag = document.createElement('div');
        new_almond_tag.id = "almond-status";
        new_almond_tag.style.display = "none";
        document.body.appendChild(new_almond_tag);
    };

    return document.getElementById('almond-status');
}

export {checkAlmondStatus, updateAlmondStatus};
