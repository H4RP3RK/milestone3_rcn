/*-question_details.html - btn scrolls to Contacts section-*/
function scrollContacts() {
    let elmnt = document.getElementById("contacts");
    elmnt.scrollIntoView();
    elmnt.classList.toggle("border-glow");
}

/*-member_home.html - btn scrolls to Questions section-*/
function scrollQuestions() {
    let elmnt = document.getElementById("questions");
    elmnt.scrollIntoView();
    elmnt.classList.toggle("border-glow");
}