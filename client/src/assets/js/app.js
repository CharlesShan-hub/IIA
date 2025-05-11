import 'jquery';
import jQuery from 'jquery';
import Waves from 'node-waves';


!function(t){
    "use strict";
    function s(e) {
        1 == t("#light-mode-switch").prop("checked") && "light-mode-switch" === e ? (t("#dark-mode-switch").prop("checked", !1), t("#rtl-mode-switch").prop("checked", !1), t("#bootstrap-style").attr("href", "assets/css/bootstrap.min.css"), t("#app-style").attr("href", "assets/css/app.min.css"), sessionStorage.setItem("is_visited", "light-mode-switch")) : 1 == t("#dark-mode-switch").prop("checked") && "dark-mode-switch" === e ? (t("#light-mode-switch").prop("checked", !1), t("#rtl-mode-switch").prop("checked", !1), t("#bootstrap-style").attr("href", "assets/css/bootstrap-dark.min.css"), t("#app-style").attr("href", "assets/css/app-dark.min.css"), sessionStorage.setItem("is_visited", "dark-mode-switch")) : 1 == t("#rtl-mode-switch").prop("checked") && "rtl-mode-switch" === e && (t("#light-mode-switch").prop("checked", !1), t("#dark-mode-switch").prop("checked", !1), t("#bootstrap-style").attr("href", "assets/css/bootstrap.min.css"), t("#app-style").attr("href", "assets/css/app-rtl.min.css"), sessionStorage.setItem("is_visited", "rtl-mode-switch"))
    }
    function e() {
        document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement || (console.log("pressed"), t("body").removeClass("fullscreen-enable"))
    }
    var n;
    t("#side-menu").metisMenu(),

    t(function() {
        t('[data-toggle="tooltip"]').tooltip()
    }),
    t(function() {
        t('[data-toggle="popover"]').popover()
    })
    window.sessionStorage && ((n = sessionStorage.getItem("is_visited")) ? (t(".right-bar input:checkbox").prop("checked", !1), t("#" + n).prop("checked", !0), s(n)) : sessionStorage.setItem("is_visited", "light-mode-switch")),
    t("#light-mode-switch, #dark-mode-switch, #rtl-mode-switch").on("change",
    function(e) {
        s(e.target.id)
    }),
    t(window).on("load",
    function() {
        t("#status").fadeOut(),
        t("#preloader").delay(350).fadeOut("slow")
    }),
    Waves.init()
}(jQuery);
