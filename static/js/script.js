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

/*-member_list.html - searches through list of members by name, employer or job title-*/
function search() {
    const memberNames = Array.from(document.querySelectorAll(".name"));
    const inputName = document.querySelector("#member_name").value.toLowerCase();
    console.log(memberNames);

    memberNames.forEach((name) => {
        nameId = name.innerText;
        memberCard = document.querySelector(".member")

        if (nameId.toLowerCase().includes(inputName)) {
            console.log(inputName);
            console.log(nameId);
            name.parentElement.style.display = "";
        }
        else {
            console.log(`Does not match ${nameId}`);
            name.parentElement.style.display = "none";
        }
    })
}

/*--Bootstrap Tabs--*/
$('#myTab a').on('click', function (e) {
  e.preventDefault()
  $(this).tab('show')
})
