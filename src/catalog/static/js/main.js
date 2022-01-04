// Ingredient Formset
const ingredientForm = document.querySelector("#emptyIngredient"),
      addIngredientBtn = document.querySelector("#addIngredient"),
      ingredientFormSet = document.querySelector("#ingredientFormSet");

function addIngredientForm() {
    newFormNumber = ingredientFormSet.querySelectorAll("#ingredientForm").length;
    document.querySelector("#id_ingredient-TOTAL_FORMS").value = newFormNumber + 1;

    newForm = ingredientForm.cloneNode(true);
    newForm.innerHTML = newForm.innerHTML.replaceAll('__prefix__', newFormNumber);
    removeBtn = newForm.querySelector("#removeIngredient");
    removeBtn.setAttribute('onclick', removeBtn.getAttribute('onclick').replace('__prefix__', newFormNumber));
    newForm.setAttribute('form-number', newFormNumber);
    newForm.removeAttribute('style');
    newForm.id = "ingredientForm";
    ingredientFormSet.appendChild(newForm);
}

addIngredientBtn.addEventListener('click', addIngredientForm)

function removeIngredientForm(formNumber) {
    form = ingredientFormSet.querySelector(`#ingredientForm[form-number="${formNumber}"]`);
    number = Number(form.getAttribute('form-number'));
    form.remove();
    for (form of ingredientFormSet.children) {
        if (form.getAttribute('form-number') > number) {
            form.setAttribute('form-number', form.getAttribute('form-number') - 1);
            for (child of form.children) {
                for (field of child.children) {
                    if (field.getAttribute('for') != null) {
                        newFor = field.getAttribute('for').replace(/ingredient-\d/g, `ingredient-${number}`);
                        field.setAttribute('for', newFor);
                    }
                    if (field.getAttribute('name') != null) {
                        newName = field.getAttribute('name').replace(/ingredient-\d/g, `ingredient-${number}`);
                        field.setAttribute('name', newName);
                    }
                    if (field.id != null) {
                        newId = field.id.replace(/ingredient-\d/g, `ingredient-${number}`);
                        field.id = newId;
                    }
                }
                if (child.getAttribute('onclick') != null) {
                    newOnclick = `removeIngredientForm(${number})`;
                    child.setAttribute('onclick', newOnclick);
                }    
            }
            number += 1;
        }
    }
    document.querySelector("#id_ingredient-TOTAL_FORMS").value -= 1;
}


// Direction Formset
const directionForm = document.querySelector("#emptyDirection"),
      addDirectionBtn = document.querySelector("#addDirection"),
      directionFormSet = document.querySelector("#directionFormSet");

function addDirectionForm() {
    newFormNumber = directionFormSet.querySelectorAll("#directionForm").length;
    document.querySelector("#id_direction-TOTAL_FORMS").value = newFormNumber + 1;

    newForm = directionForm.cloneNode(true);
    newForm.innerHTML = newForm.innerHTML.replaceAll('__prefix__', newFormNumber);
    removeBtn = newForm.querySelector("#removeDirection");
    removeBtn.setAttribute('onclick', removeBtn.getAttribute('onclick').replace('__prefix__', newFormNumber));
    newForm.setAttribute('form-number', newFormNumber);
    newForm.removeAttribute('style');
    newForm.id = "directionForm";
    directionFormSet.appendChild(newForm);
}

addDirectionBtn.addEventListener('click', addDirectionForm)

function removeDirectionForm(formNumber) {
    form = directionFormSet.querySelector(`#directionForm[form-number="${formNumber}"]`);
    number = Number(form.getAttribute('form-number'));
    form.remove();
    for (form of directionFormSet.children) {
        if (form.getAttribute('form-number') > number) {
            form.setAttribute('form-number', form.getAttribute('form-number') - 1);
            for (child of form.children) {
                for (field of child.children) {
                    if (field.getAttribute('for') != null) {
                        newFor = field.getAttribute('for').replace(/direction-\d/g, `direction-${number}`);
                        field.setAttribute('for', newFor);
                    }
                    if (field.getAttribute('name') != null) {
                        newName = field.getAttribute('name').replace(/direction-\d/g, `direction-${number}`);
                        field.setAttribute('name', newName);
                    }
                    if (field.id != null) {
                        newId = field.id.replace(/direction-\d/g, `direction-${number}`);
                        field.id = newId;
                    }
                }
                if (child.getAttribute('onclick') != null) {
                    newOnclick = `removeDirectionForm(${number})`;
                    child.setAttribute('onclick', newOnclick);
                }    
            }
            number += 1;
        }
    }
    document.querySelector("#id_direction-TOTAL_FORMS").value -= 1;
}
