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
/*-
function search() {
    const memberNames = Array.from(document.querySelectorAll(".name"));
    const inputName = document.querySelector("#member_name").value.toLowerCase();
    const accordion = document.querySelector("#accordion");

    console.log(memberNames);
    accordion.innerHTML = "";

    memberNames.forEach((name) => {
        nameId = name.innerText;
        accordionCard = `
                    <div class="card member">
                        <div class="card-header" id="${name.id}">
                            <div class="mb-0 row align-items-center">
                                <div class="col-sm-4">
                                    <h5 class="font-blue name">${nameId}</h5>
                                </div>
                                <div class="col-sm-4">
                                    <span></span>
                                </div>
                                <div class="col-sm-4">
                                    <button class="btn blue-btn btn-link accordion-btn collapsed" data-toggle="collapse" data-target="#collapse${name.id}" aria-expanded="false" aria-controls="collapse${name.id}">
                                    Summary
                                    </button>
                                    <a class="blue-btn btn accordion-btn" href="#">Full details</a>
                                </div>
                            </div>
                        </div>
                        <div id="collapse${name.id}" class="collapse" aria-labelledby="heading${name.id}" data-parent="#accordion">
                            <div class="card-body">
                            </div>
                        </div>
                    </div>  `

        if (nameId.toLowerCase().includes(inputName)) {
            console.log(inputName);
            console.log(nameId);
            accordion.insertAdjacentHTML("beforeend", accordionCard)
        }
        else {
            console.log(`Does not match ${nameId}`);
        }
    })
    
}
-*/


function search() {
    const memberNames = Array.from(document.querySelectorAll(".name"));
    const inputName = document.querySelector("#member_name").value.toLowerCase();
    const accordion = document.querySelector("#accordion");
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
