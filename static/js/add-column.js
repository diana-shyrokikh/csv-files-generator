const addMoreBtn = document.getElementById("add-more");
const totalNewForms = document.getElementById(
    "id_schema_column-TOTAL_FORMS"
);
addMoreBtn.addEventListener("click", add_new_form);

function add_new_form(event) {
    if (event) {
        event.preventDefault();
    }

    const currentChildForms = document.getElementsByClassName(
        "children-form"
    );
    const currentFormCount = currentChildForms.length;
    const regex = new RegExp("__prefix__", "g");


    const formCopyTarget = document.getElementById(
        "children-form-table"
    );
    const copyEmptyFormEl = document.getElementById(
        "empty-form"
    ).cloneNode(true);

    copyEmptyFormEl.setAttribute("class", "children-form");
    copyEmptyFormEl.setAttribute("style", "display: true");
    copyEmptyFormEl.setAttribute("id", `child-${currentFormCount}`);
    copyEmptyFormEl.innerHTML = copyEmptyFormEl.innerHTML.replace(
        regex, currentFormCount
    );

    totalNewForms.setAttribute("value", currentFormCount + 1);

    formCopyTarget.append(copyEmptyFormEl);
}