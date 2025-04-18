// Example data: Replace this with actual data from your quiz logic
const quizResults = [
    {
        question: "The Password Dilemma",
        yourAnswer: "12345678",
        correctAnswer: "T!m#Sp@rk_921 ✅",
        isCorrect: false
    },
    {
        question: "Phishy Email",
        yourAnswer: "Check sender & hover over the link ✅",
        correctAnswer: "Check sender & hover over the link ✅",
        isCorrect: true
    },
    {
        question: "Café Wi-Fi Choice",
        yourAnswer: "Log into online banking",
        correctAnswer: "Use VPN and browse normally ✅",
        isCorrect: false
    },
    {
        question: "Download Trap",
        yourAnswer: "Close the window ✅",
        correctAnswer: "Close the window ✅",
        isCorrect: true
    },
    {
        question: "Privacy Check",
        yourAnswer: "That’s fine, everyone does it",
        correctAnswer: "Make them visible only to friends ✅",
        isCorrect: false
    }
];

// Populate the scorecard table
const scoreTableBody = document.getElementById('score-table-body');

quizResults.forEach((result, index) => {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${index + 1}. ${result.question}</td>
        <td>${result.yourAnswer}</td>
        <td>${result.correctAnswer}</td>
        <td style="color: ${result.isCorrect ? 'green' : 'red'};">
            ${result.isCorrect ? 'Correct' : 'Incorrect'}
        </td>
    `;
    scoreTableBody.appendChild(row);
});