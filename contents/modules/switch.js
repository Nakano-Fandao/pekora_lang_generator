// Variables
const ad_kwd_list = ["googleads", "aswift", "banner", "adsystem", "ad"];
const iframe_tags = document.getElementsByTagName('iframe');



const switchImgs = () => {

    switchAdFrame();


    console.log("Switching images completed")
    import("./loading.js").then( module => module.removeLoading() );
    import("./almond_status.js")
        .then( module => module.updateAlmondStatus("image", true) );
}

const returnOriginalImgs = () => {
    import("./almond_status.js")
        .then( module => module.updateAlmondStatus("image", false) );

}

const switchAdFrame = () => {
    const ad_frame = Array.from(iframe_tags)
        .filter( item => tagFilter(item, ad_kwd_list) );
}

const tagFilter = (item, kwd_list) => {
    const id_bool = kwd_list.map( kwd => item.id.includes(kwd) ).includes(true);
    const class_bool = kwd_list.map( kwd => item.class.includes(kwd) ).includes(true);
    const src_bool = kwd_list.map( kwd => item.src.includes(kwd) ).includes(true);

    return [id_bool, class_bool, src_bool].includes(true);
}



export {switchImgs, returnOriginalImgs};
