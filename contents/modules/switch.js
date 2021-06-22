// Variables
const ad_kwd_list = ["googleads", "aswift", "banner", "adsystem", "ad"];
const iframe_tags = document.getElementsByTagName('iframe');
const ad_cover_dir = chrome.extension.getURL("../images/ad-covers/");
const img_urls = [ad_cover_dir+"pekora.png", ad_cover_dir+"carrot.png"];

const switchImgs = () => {
    switchAdFrame();
    console.log("Switching images completed")

    Promise.all([
        import("./loading.js"),
        import("./almond_status.js")
    ]).then( (modules) => {
        modules[0].removeLoading();
        modules[1].updateAlmondStatus("image", true);
    });
}

const returnOriginalImgs = () => {
    removeAdCover();

    Promise.all([
        import("./loading.js"),
        import("./almond_status.js")
    ]).then( (modules) => {
        modules[0].removeLoading();
        modules[1].updateAlmondStatus("image", false);
    });
}

// iframe ad ----------------------------------------
const switchAdFrame = () => {
    const ad_frame_tags = Array.from(iframe_tags).filter( item => tagFilter(item, ad_kwd_list) );
    ad_frame_tags.map( ad_frame => createAdCover(ad_frame) );
}
const createAdCover = (target_elem) => {
    if (target_elem.style.display == 'none') { return; }

    const ad_cover = document.createElement('div');
    const img_tag = document.createElement('img');
    const img_url = img_urls[Math.floor(Math.random()*img_urls.length)];
    img_tag.src             = img_url;
    img_tag.alt             = "Pekora cover";
    img_tag.style.height    = target_elem.height + "px";
    img_tag.style.width     = target_elem.width + "px";
    ad_cover.classList.add("ad-cover");
    ad_cover.appendChild(img_tag);
    target_elem.parentNode.insertBefore(ad_cover, target_elem);
}
const removeAdCover = () => {
    Array.from( document.getElementsByClassName('ad-cover') )
        .map( ad_cover => ad_cover.remove() );
}
const tagFilter = (item, kwd_list) => {
    const id_bool = kwd_list.map( kwd => item.id.includes(kwd) ).includes(true);
    const class_bool = kwd_list.map( kwd => Array.from(item.classList).includes(kwd) ).includes(true);
    const src_bool = kwd_list.map( kwd => item.src.includes(kwd) ).includes(true);

    return [id_bool, class_bool, src_bool].includes(true);
}

// Export functions ---------------------------
export {switchImgs, returnOriginalImgs};
