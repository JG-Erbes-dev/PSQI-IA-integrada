document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        if (this.checked) {
            document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
                if (cb !== this) {
                    cb.checked = false;
                }
            });
        }
    });
});
function formatDate(input) {
    let value = input.value.replace(/\D/g, '');

    if (value.length > 2) {
        value = value.slice(0, 2) + '/' + value.slice(2);
    }
    if (value.length > 5) {
        value = value.slice(0, 5) + '/' + value.slice(5);
    }

    input.value = value;

    updateDisplay(value);
}

function updateDisplay(value) {
    let displayValue = '__/__/____';
    let day = value.slice(0, 2); 
    let month = value.slice(3, 5); 
    let year = value.slice(6); 

    if (day.length === 1) {
        displayValue = displayValue.replace('__', `<u>${day}</u>_`);
    } else if (day.length === 2) {
        displayValue = displayValue.replace('__', `<u>${day}</u>`);
    }
    if (month.length === 1) {
        displayValue = displayValue.replace('__', `<u>${month}</u>_`);
    } else if (month.length === 2) {
        displayValue = displayValue.replace('__', `<u>${month}</u>`);
    }
    if (year.length === 1) {
        displayValue = displayValue.replace('____', `<u>${year}</u>___`);
    } else if (year.length === 2) {
        displayValue = displayValue.replace('____', `<u>${year}</u>__`);
    } else if (year.length === 3) {
        displayValue = displayValue.replace('____', `<u>${year}</u>_`);
    } else if (year.length === 4) {
        displayValue = displayValue.replace('____', `<u>${year}</u>`);
    }

    document.getElementById("date-output").innerHTML = displayValue + (value.length = 10 ? '.': '');
}


document.addEventListener("DOMContentLoaded", function() {
    const dateInput = document.getElementById("date");
    updateDisplay(dateInput.value); 
});

updateDisplay(''); 

document.getElementById("date").addEventListener("input", function() {
    updateDisplay(this.value);
});
function updateTextPlaceholder(input) {
    let value = input.value;

    let placeholder = '__________________.';
    let filledPlaceholder = placeholder;

    for (let i = 0; i < value.length && i < 18; i++) { 
        filledPlaceholder = filledPlaceholder.replace('_', `<u>${value[i]}</u>`);
    }

    document.getElementById("text-output").innerHTML = filledPlaceholder;

    input.setAttribute('placeholder', filledPlaceholder.replace(/<u>|<\/u>/g, ''));
}

document.addEventListener("DOMContentLoaded", function() {
    const textInput = document.getElementById("text-input");
    updateTextPlaceholder(textInput);
});