//test
//console.log("hello Prabhat");
// **********set date****************
const date = (document.getElementById("date").innerHTML = new Date().getFullYear());

//***********nav toggle************/

const navBtn = document.getElementById("nav_toggle");
const navLink = document.getElementById("nav_links");

//console.log(navBtn);
//console.log(navLink);

//**********add EventListner************/

navBtn.addEventListener("click", () => {
    navLink.classList.toggle("show_links");
});

//*********** nav fixed **************/
const navbar = document.querySelector(".navbar");

window.addEventListener("scroll", () =>{
    //136.44
    if(window.pageYOffset > 5){
        navbar.classList.add('fixed');
    }
    else
    {
        navbar.classList.remove('fixed');
    }
})

//************smooth scroll**************/

const scrollLink = document.querySelectorAll(".scroll_link");

scrollLink.forEach((link)=>{
    link.addEventListener("click",(e)=>{
        e.preventDefault();
        //console.log("hello you clicked a link");
        navLink.classList.remove("show_links");
        const id = e.target.getAttribute("href").slice(1);
        const element = document.getElementById(id);

        //position
        let position
    //    if(navbar.classList.contains("fixed")){
            position = element.offsetTop - 75;
      //  }
        window.scrollTo({
            left: 0,
            top: position,
            behavior: "smooth"
        });

    });
});



















