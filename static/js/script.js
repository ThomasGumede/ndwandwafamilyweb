
const navbarItems = document.getElementById("navbar_items");
const navbar = document.getElementById("navbar");
const menu = document.getElementById("menu");

const nav_btn = document.getElementById("navbar-button")



menu.addEventListener("click", function(){
  
  if (navbarItems.classList.contains("dont-show-mobile-navbar")) {
    navbarItems.classList.remove("dont-show-mobile-navbar");
    navbarItems.classList.add("show-mobile-navbar");
    
  } else {
    navbarItems.classList.remove("show-mobile-navbar");
    navbarItems.classList.add("dont-show-mobile-navbar");
  }
})

window.addEventListener("scroll", function () {

  if (window.scrollY >= 100) {
    // alert(window.scrollY)
    navbar.classList.remove("navbar_not_scroll");
    navbar.classList.add("navbar_on_scroll");

  } else {
    navbar.classList.remove("navbar_on_scroll");
    navbar.classList.add("navbar_not_scroll");
  }
});

if (navbarItems.classList.contains("show-mobile-navbar"))
{
  window.addEventListener("click", function () {
    navbarItems.classList.remove("show-mobile-navbar");
    navbarItems.classList.add("dont-show-mobile-navbar");
  });
}