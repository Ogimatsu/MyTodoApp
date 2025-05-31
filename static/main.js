// 一覧画面の検索ボタン押下時、モーダルを開いたままにする
document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    // action=searchがURLにあればモーダルを開く
    if (urlParams.get("action") === "search") {
        const searchCollapse = document.getElementById("collapseSearch");
        searchCollapse.classList.add("show");
        }
    });

// 一覧画面のクリアボタン押下時に、入力内容のみクリアし、モーダルを閉じないようにする
function resetForm() {
    const form = document.getElementById("searchForm");
    form.reset();

    form.querySelectorAll("input, select").forEach(el => {
      if (el.type !== "submit" && el.type !== "button") {
        el.value = "";
      }
    });

    // action=searchをURLから除外する
    const url = new URL(window.location);
    url.searchParams.delete("action");
    history.replaceState({}, document.title, url);
}