const quizContainer = document.getElementById('quiz-container');
const questionTitle = document.getElementById('question-title');
const questionDescription = document.getElementById('question-description');
const optionsContainer = document.getElementById('options');
const feedbackContainer = document.getElementById('feedback');
const feedbackMessage = document.getElementById('feedback-message');
const correctAnswer = document.getElementById('correct-answer');
const nextQuestionBtn = document.getElementById('next-question-btn');

const questions = [
    {
        title: "The Password Dilemma",
        description: "Scenario: You’re signing up for a new website. Which password do you choose?",
        options: ["12345678", "john@1998", "T!m#Sp@rk_921 ✅", "password123"],
        correct: 2
    },
    {
        title: "Phishy Email",
        description: "Scenario: You get this email: “🚨 Your account is locked! Click here to reset it now!” What do you do?",
        options: ["Click the link immediately", "Ignore it", "Check sender & hover over the link ✅", "Reply asking for more info"],
        correct: 2
    },
    {
        title: "Café Wi-Fi Choice",
        description: "Scenario: You’re on public Wi-Fi. Which of these is safest?",
        options: ["Log into online banking", "Turn off your VPN", "Use VPN and browse normally ✅", "Share the hotspot with strangers"],
        correct: 2
    },
    {
        title: "Download Trap",
        description: "Scenario: You visit a sketchy site and see “Install this update to continue.” What now?",
        options: ["Click and install", "Check the file name and download anyway", "Close the window ✅", "Disable antivirus temporarily"],
        correct: 2
    },
    {
        title: "Privacy Check",
        description: "Scenario: Your birthday and phone number are public on your social media profile.",
        options: ["That’s fine, everyone does it", "Make them visible only to friends ✅", "Add more personal info", "Doesn’t matter, it’s harmless"],
        correct: 1
    }
];

let currentQuestionIndex = 0;
let score = 0; // Track the user's score

function loadQuestion(index) {
    const question = questions[index];
    questionTitle.textContent = question.title;
    questionDescription.textContent = question.description;
    optionsContainer.innerHTML = question.options
        .map((option, i) => `<button class="quiz-option" data-index="${i}">${option}</button>`)
        .join('');
    feedbackContainer.classList.add('hidden');
    nextQuestionBtn.classList.add('hidden');

    document.querySelectorAll('.quiz-option').forEach((btn) => {
        btn.addEventListener('click', (e) => {
            const selected = parseInt(e.target.getAttribute('data-index'));
            if (selected === question.correct) {
                feedbackMessage.textContent = "Correct! Great job!";
                feedbackMessage.style.color = "green";
                score++; // Increment score for a correct answer
            } else {
                feedbackMessage.textContent = "Incorrect. Try to be more cautious!";
                feedbackMessage.style.color = "red";
            }
            correctAnswer.textContent = `Correct Answer: ${question.options[question.correct]}`;
            feedbackContainer.classList.remove('hidden');
            nextQuestionBtn.classList.remove('hidden');
        });
    });
}

nextQuestionBtn.addEventListener('click', () => {
    currentQuestionIndex++;
    if (currentQuestionIndex < questions.length) {
        loadQuestion(currentQuestionIndex);
    } else {
        displayScore(); // Display the final score
    }
});

function displayScore() {
    quizContainer.innerHTML = `
        <h2>Quiz Complete!</h2>
        <p>Your Score: ${score} / ${questions.length}</p>
        <p>Thank you for taking the quiz!</p>
    `;
}

// Load the first question
loadQuestion(currentQuestionIndex);