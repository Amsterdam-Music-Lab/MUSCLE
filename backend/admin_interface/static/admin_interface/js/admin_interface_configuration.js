// // on load
// document.addEventListener('DOMContentLoaded', function() {

//     // append color behind input
//     const inputs = document.querySelectorAll('input[type="color"]');
//     inputs.forEach(input => {
//         appendColorBehindInput(input);
//     }



//     // add event listeners to all inputs


// });

// function appendColorBehindInput(input) {
//     const parentEl = input.parentElement;
//     const color = input.value;
//     const colorEl = document.createElement('div');
//     colorEl.style.width = '20px';
//     colorEl.style.height = '20px';
//     colorEl.style.backgroundColor = color;
//     colorEl.style.border = '1px solid black';
//     colorEl.style.borderRadius = '50%';
//     colorEl.style.marginLeft = '10px';
//     parentEl.appendChild(colorEl);
// }