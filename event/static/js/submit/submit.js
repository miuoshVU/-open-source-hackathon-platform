const MAX_WIDTH = decideCurr()
function onPage(sizes){
    xl = window.matchMedia("(min-width: 999px) and (max-width: 3000px)");
    l = window.matchMedia("(min-width: 760px) and (max-width: 999px)");
    if(xl.matches){
        document.getElementById("width-control").style.maxWidth = sizes[0]
    }else if(l.matches){
        document.getElementById("width-control").style.maxWidth = sizes[1]
    }
    return
}

function returnOrigin(){
    document.getElementById("width-control").style.maxWidth = MAX_WIDTH
}

function decideCurr(){
    let curr = "90%"
    if(window.matchMedia("(min-width: 999px) and (max-width: 3000px)").matches){
        curr = "60%"
    }else if(window.matchMedia("(min-width: 760px) and (max-width: 999px)").matches){
        curr = "80%"
    }else if(window.matchMedia("(min-width: 530px) and (max-width: 759px)").matches){
        curr = "85%"
    }else if(window.matchMedia("(min-width: 359px) and (max-width: 376px)").matches){
        curr = "85%"
    }else if(window.matchMedia("(max-width: 290px)").matches){
        curr = "100%"
    }
    return curr
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const wholeForm = document.querySelector(".form-whole")
const formPages = [...wholeForm.querySelectorAll(".form-page")]
let pageInfo = {
    currentPage: -1,
    pageValidationStatus: true,
    individualValidation: new Map([
        [0, true],
        [1, true],
        [2, false],
        [3, true],
        [4, true]
    ]),
    errors: new Map([
        [0, []],
        [1, []],
        [2, []],
        [3, []]
    ])
};
if (pageInfo.currentPage < 0) {
    pageInfo.currentPage = 0;
    showCurrentPage();
}
pageInfo.currentPage = formPages.findIndex(page => {
    return !page.classList.contains("d-none")
})

wholeForm.addEventListener("click", event => {


    let increment = 0
    pageInfo.pageValidationStatus = true
    if (event.target.matches("[data-next-button]")) {
        increment = 1
        const inputFields = [...formPages[pageInfo.currentPage].querySelectorAll("input")]
        pageInfo.pageValidationStatus = inputFields.every(input => input.reportValidity())
    } else if (event.target.matches("[data-previous-button]")) {
        increment = -1
    } if (increment == null) return


    generalErrorText = document.getElementById("error-reminder-container");
    if (pageInfo.pageValidationStatus && pageInfo.individualValidation.get(pageInfo.currentPage)) {
        generalErrorText.classList.add("d-none")
        pageInfo.currentPage += increment;
        showCurrentPage();

    } else if (event.target.matches("[data-previous-button]")) {
        generalErrorText.classList.add("d-none")
        pageInfo.currentPage += increment;
        showCurrentPage();
    } else {
        generalErrorText.classList.add("d-none") 
    }
})


function showCurrentPage() {
    formPages.forEach((page, index) => {
        page.classList.toggle("d-none", index != pageInfo.currentPage)
    })
    if (pageInfo.currentPage == 4) {
        onPage(["40%", "60%"]);
    } else {
        returnOrigin();
    }
}