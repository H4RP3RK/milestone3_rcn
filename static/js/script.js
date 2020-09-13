/*-question_details.html - btn scrolls to Contacts section-*/
function scrollContacts() {
    let elmnt = document.querySelector("#contacts");
    elmnt.scrollIntoView();
    elmnt.classList.toggle("border-glow");
}

/*-member_home.html - btn scrolls to Questions section-*/
function scrollQuestions() {
    let elmnt = document.querySelector("#questions");
    elmnt.scrollIntoView();
    elmnt.classList.toggle("border-glow");
}

/*-member_list.html - search through members-*/
function search() {
    const member_names = document.querySelectorAll("h5");
    const inputName = document.querySelector("#member_name").nodeValue.toLowerCase();

    
}