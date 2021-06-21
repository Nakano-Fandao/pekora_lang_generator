// Variables
const ad_kwd_list = ["googleads", "aswift", "banner", "adsystem", "ad"];
const iframe_tags = document.getElementsByTagName('iframe');
const ad_cover_dir = chrome.extension.getURL("../images/ad-covers/");
const img_urls = [ad_cover_dir+"pekora.png", ad_cover_dir+"carrot.png"];

const switchImgs = () => {
    switchAdFrame();
    console.log("Switching images completed")

    import("./loading.js").then( module => module.removeLoading() );
    import("./almond_status.js")
        .then( module => module.updateAlmondStatus("image", true) );
}

const returnOriginalImgs = () => {
    Array.from( document.getElementsByClassName('ad-cover') )
        .map( ad_cover => ad_cover.remove() );

    import("./loading.js").then( module => module.removeLoading() );
    import("./almond_status.js")
        .then( module => module.updateAlmondStatus("image", false) );

}

// iframe ad ----------------------------------------
const switchAdFrame = () => {
    const ad_frame_tags = getAdFrame();
    ad_frame_tags.map( ad_frame => {
        createAdCover(ad_frame);
    })
}
const getAdFrame = () => {
    return Array.from(iframe_tags).filter( item => tagFilter(item, ad_kwd_list) );
}
const createAdCover = (target_elem) => {
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
const removeAdcCover = (target_elem) => {

}
const tagFilter = (item, kwd_list) => {
    const id_bool = kwd_list.map( kwd => item.id.includes(kwd) ).includes(true);
    const class_bool = kwd_list.map( kwd => Array.from(item.classList).includes(kwd) ).includes(true);
    const src_bool = kwd_list.map( kwd => item.src.includes(kwd) ).includes(true);

    return [id_bool, class_bool, src_bool].includes(true);
}

// Export functions ---------------------------
export {switchImgs, returnOriginalImgs};
