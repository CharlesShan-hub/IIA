<template>
  <body data-sidebar="dark" class>
    <AppHeader />
    <div id="layout-wrapper">
      <AppSidebar />
      <div class="main-content">
        <DashboardPage />
        <AppFooter />
      </div>
    </div>
    <AppRightbar />
  </body>
</template>

<script>
import AppHeader from './Header.vue'
import AppSidebar from './Sidebar.vue'
import AppRightbar from './Rightbar.vue'
import AppFooter from './Footer.vue'
import DashboardPage from './Dashboard.vue'

export default {
  name: 'MainPage',
  components: {
    AppHeader,
    AppSidebar,
    AppRightbar,
    AppFooter,
    DashboardPage,
  },
}

  import jQuery from 'jquery'
  window.jQuery = window.$ = jQuery
  import 'bootstrap' // 4.5.3
  import 'metismenu'
  import 'simplebar'
  import Waves from 'node-waves'
  // import '@/assets/libs/peity/jquery.peity.js'
  import 'chartist'
  import 'chartist-plugin-tooltip'

  !function(t) {
      "use strict";
      t(document).ready(function() {
          // function s(e) {
          //     1 == t("#light-mode-switch").prop("checked") && "light-mode-switch" === e ? (t("#dark-mode-switch").prop("checked", !1), t("#rtl-mode-switch").prop("checked", !1), t("#bootstrap-style").attr("href", "assets/css/bootstrap.min.css"), t("#app-style").attr("href", "assets/css/app.min.css"), sessionStorage.setItem("is_visited", "light-mode-switch")) : 1 == t("#dark-mode-switch").prop("checked") && "dark-mode-switch" === e ? (t("#light-mode-switch").prop("checked", !1), t("#rtl-mode-switch").prop("checked", !1), t("#bootstrap-style").attr("href", "assets/css/bootstrap-dark.min.css"), t("#app-style").attr("href", "assets/css/app-dark.min.css"), sessionStorage.setItem("is_visited", "dark-mode-switch")) : 1 == t("#rtl-mode-switch").prop("checked") && "rtl-mode-switch" === e && (t("#light-mode-switch").prop("checked", !1), t("#dark-mode-switch").prop("checked", !1), t("#bootstrap-style").attr("href", "assets/css/bootstrap.min.css"), t("#app-style").attr("href", "assets/css/app-rtl.min.css"), sessionStorage.setItem("is_visited", "rtl-mode-switch"))
          // }
          function s(themeName) {
              console.log("themeName: ", themeName);
              var isLightMode = themeName === "light-mode-switch";
              var isDarkMode = themeName === "dark-mode-switch";
              var isRtlMode = themeName === "rtl-mode-switch";

              // Reset all switches
              t("#light-mode-switch").prop("checked", false);
              t("#dark-mode-switch").prop("checked", true);
              t("#rtl-mode-switch").prop("checked", false);

              if (isLightMode) {
                t("#bootstrap-style").attr("href", "assets/css/bootstrap.min.css");
                t("#app-style").attr("href", "assets/css/app.min.css");
              } else if (isDarkMode) {
                t("#bootstrap-style").attr("href", "assets/css/bootstrap-dark.min.css");
                t("#app-style").attr("href", "assets/css/app-dark.min.css");
              } else if (isRtlMode) {
                t("#bootstrap-style").attr("href", "assets/css/bootstrap.min.css");
                t("#app-style").attr("href", "assets/css/app-rtl.min.css");
              }

              sessionStorage.setItem("is_visited", themeName);
          }
          function e() {
              document.webkitIsFullScreen || document.mozFullScreen || document.msFullscreenElement || (console.log("pressed"), t("body").removeClass("fullscreen-enable"))
          }
          t("#side-menu").metisMenu(),
          t("#vertical-menu-btn").on("click",
          function(e) {
              e.preventDefault(),
              t("body").toggleClass("sidebar-enable"),
              992 <= t(window).width() ? t("body").toggleClass("vertical-collpsed") : t("body").removeClass("vertical-collpsed")
          }),
          t("#sidebar-menu a").each(function() {
              var e = window.location.href.split(/[?#]/)[0];
              this.href == e && (t(this).addClass("active"), t(this).parent().addClass("mm-active"), t(this).parent().parent().addClass("mm-show"), t(this).parent().parent().prev().addClass("mm-active"), t(this).parent().parent().parent().addClass("mm-active"), t(this).parent().parent().parent().parent().addClass("mm-show"), t(this).parent().parent().parent().parent().parent().addClass("mm-active"))
          }),
          t(".navbar-nav a").each(function() {
              var e = window.location.href.split(/[?#]/)[0];
              this.href == e && (t(this).addClass("active"), t(this).parent().addClass("active"), t(this).parent().parent().addClass("active"), t(this).parent().parent().parent().addClass("active"), t(this).parent().parent().parent().parent().addClass("active"), t(this).parent().parent().parent().parent().parent().addClass("active"))
          }),
          t('[data-toggle="fullscreen"]').on("click",
          function(e) {
              e.preventDefault(),
              t("body").toggleClass("fullscreen-enable"),
              document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement ? document.cancelFullScreen ? document.cancelFullScreen() : document.mozCancelFullScreen ? document.mozCancelFullScreen() : document.webkitCancelFullScreen && document.webkitCancelFullScreen() : document.documentElement.requestFullscreen ? document.documentElement.requestFullscreen() : document.documentElement.mozRequestFullScreen ? document.documentElement.mozRequestFullScreen() : document.documentElement.webkitRequestFullscreen && document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT)
          }),
          document.addEventListener("fullscreenchange", e),
          document.addEventListener("webkitfullscreenchange", e),
          document.addEventListener("mozfullscreenchange", e),
          t(".right-bar-toggle").on("click",
          function() {
              t("body").toggleClass("right-bar-enabled")
          }),
          t(document).on("click", "body",
          function(e) {
              0 < t(e.target).closest(".right-bar-toggle, .right-bar").length || t("body").removeClass("right-bar-enabled")
          }),
          t(".dropdown-menu a.dropdown-toggle").on("click",
          function() {

              return t(this).next().hasClass("show") || t(this).parents(".dropdown-menu").first().find(".show").removeClass("show"),
              t(this).next(".dropdown-menu").toggleClass("show"),
              !1
          }),
          t(function() {
              t('[data-toggle="tooltip"]').tooltip()
          }),
          t(function() {
              t('[data-toggle="popover"]').popover()
          });
          // window.sessionStorage && ((n = sessionStorage.getItem("is_visited")) ? (t(".right-bar input:checkbox").prop("checked", !1), t("#" + n).prop("checked", !0), s(n)) : sessionStorage.setItem("is_visited", "light-mode-switch")),
          if (window.sessionStorage) {
              const currentTheme = sessionStorage.getItem("is_visited");
              if (currentTheme) {
                  t(".right-bar input:checkbox").prop("checked", false);
                  t("#" + currentTheme).prop("checked", true);
                  s(currentTheme);
              } else {
                  sessionStorage.setItem("is_visited", "light-mode-switch");
              }
          }
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
      });
  }(jQuery)
</script>

<style scoped>
@import '@/assets/libs/chartist/chartist.min.css';
@import '@/assets/css/bootstrap.min.css';
@import '@/assets/css/icons.min.css';
@import '@/assets/css/app.min.css';
</style>
