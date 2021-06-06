'use strict';


chrome.extension.onMessage.addListener(function(request, sender, sendResponse) {
	if (request == "Action") {
		see_pekora();
	}
});

function see_pekora() {

    // A greeting from Pekora
    alert("こんぺこ！こんぺこ！こんぺこー！ホロライブ3期生の兎田ぺこらぺこ～！");

    //  いろいろ用（ブラウザなど）
    const tag_list = ['p', 'h1', 'li', 'th', 'td', 'h2', 'h3', 'h4', 'h5', 'h6'];
    tag_list.forEach(function(tag) {
        change_peko(Array.from(document.getElementsByTagName(tag)));
    })

    // メール用
    change_peko(Array.from(document.getElementsByClassName('PlainText')));
    change_peko(Array.from(document.getElementsByClassName('allowTextCollection')));

}

const change_peko = function(list){
    list.forEach(function(item){
        early_peko(item);
        middle_peko(item);
        final_peko(item);
    });
}

const early_peko = function(item){
    item.innerText = item.innerText
        .replace("私は", "ぺこーらは")
        .replace("こんにちは", "こんぺこ")
        .replace("しかし", "でも")
        .replace("そのため", "ちゅうわけで")
        .replace("君", "野うさぎ")
        .replace("あなた", "野うさぎ")

        // よろしく系
        .replace("よろしくお願いいたします", "よろしくぺっこ～")
        .replace("よろしくお願いします", "よろしくぺっこ～")
        .replace("よろしくお願い致します", "よろしくぺっこ～")
        .replace("よろしく", "よろしくぺっこ～")

        // 分かった系
        .replace("分かりました", "おっけーぺっこ～")
        .replace("わかりました", "おっけーぺっこ～！")
        .replace("承知いたしました", "おっけーぺっこ～！")
  }
const middle_peko = function(item){
    item.innerText = item.innerText
        .replace("いただけませんでしょうか。", "できるぺこか？")
        .replace("できません", "できないぺこ")

        // ましょう系
        .replace("みましょう", "みるぺこ")
        .replace("しましょう", "する")
        .replace("りましょう", "るぺこ")
        .replace("きましょう", "くぺこ")

        
        .replace("いたします", "する")
        .replace("ございます", "ある")
        

        .replace("いきます", "いくぺこ")
        .replace("いきません", "いかないぺこ")
        .replace("しています", "する")
        .replace("できます", "できる")
        .replace("あります", "ある")
        .replace("されます", "されるぺこ")
        .replace("りました", "ったぺこ")
        .replace("にいます", "にいるぺこ")
        .replace("でしょうか", "ぺこ？")
        .replace("ですので", "ぺこなので")
        .replace("れるの", "れるぺこなの")

        // ください系
        .replace("をください", "をくれぺこ")
        .replace("てください", "てぺこ")
        
        .replace("にいました", "にいたぺこ")
        .replace("がいました", "がいたぺこ")
        .replace("いました", "ったぺこ")
        .replace("ました", "たぺこ")
        
        .replace("たので", "たぺこなので")
        .replace("るので", "るぺこなので")
        .replace("みます。", "みるぺこ！")
        .replace("ります。", "るぺこ！")
        .replace("行います", "行うぺこ！")
        .replace("います", "いるぺこ")
        .replace("できる。", "できるぺこ！")
        .replace("だろう。", "ぺこ！")
  }
const final_peko = function(item){
    item.innerText = item.innerText
        .replace("する。", "するぺこ！")
        .replace("する」", "するぺこ」")
        .replace("します", "するぺこ")
        .replace("ます", "ますぺこ")
        .replace("でしょう", "っぽいぺこ")
        .replace("です", "ぺこ")
        .replace("さい", "さいぺこ")
        .replace("れる。", "れるぺこ！")
        .replace("れる！", "れるぺこ！")
        .replace("たい。", "たいぺこ！")
        .replace("たい！", "たいぺこ！")
        .replace("たい）", "たいぺこ)")
        .replace("ない。", "ないぺこ！")
        .replace("ない！", "ないぺこ！")
        .replace("ない）", "ないぺこ）")
        .replace("ある", "あるぺこ")
        .replace("いる。", "いるぺこ！")
        .replace("いる！", "いるぺこ！")
        .replace("みた。", "みたぺこ！")
        .replace("みた！", "みたぺこ！")
        .replace("だが", "ぺこが")
        .replace("よね", "ぺこね")
        
        .replace("んだ。", "んだぺこ！")
        .replace("る。", "るぺこ！")
        .replace("た。", "たぺこ！")
        .replace("だ。", "ぺこ！")
        .replace("か。", "ぺこ？")
        
        .replace("。", "！")

  }