// Generating the HTML content for the questions page

const questions_answers = [{
    question: 'What happens when I give blood',
    answer: 'Whether you are a first-time or regular donor, the blood service must make sure that you will come to no harm by donating blood. This includes checking your blood to be sure it will be safe for the person who receives it.'
},{
    question: 'How much blood will be taken',
    answer: 'In most countries, the volume of blood taken is 450 millilitres, less than 10 per cent of your total blood volume (the average adult has 4.5 to 5 litres of blood). In some countries, a smaller volume is taken. Your body will replace the lost fluid within about 36 hours.'
},{
    question: 'Is giving blood safe',
    answer: 'Yes. Remember that you will only be accepted as a blood donor if you are fit and well. Your health and well-being are very important to the blood service. The needle and blood bag used to collect blood come in a sterile pack that cannot be reused, so the process is made as safe as possible.'
},{
    question: 'Who can give blood, and how often',
    answer: 'The criteria for donor selection varies from country to country, but blood can be donated by most people who are healthy and do not have an infection that can be transmitted through their blood. Healthy adults can give blood regularly &dash; at least twice a year. Your local blood service can tell you how frequently you can give blood.'
}]

let questionsHTML = '';

questions_answers.forEach((x) => {
    questionsHTML += `<div class="mb-4">
    <h4 class="question">${x.question}&#63;</h4>
    <p class="answer">${x.answer}</p>
    <hr>
</div>`;
}
)

document.querySelector('.js-questions-container').innerHTML = questionsHTML;