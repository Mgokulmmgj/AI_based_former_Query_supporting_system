async function askQuestion() {
    const question = document.getElementById("question").value;
    const answerBox = document.getElementById("answer");

    answerBox.innerText = "Thinking... ⏳";

    const response = await fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: question })
    });

    const data = await response.json();
    answerBox.innerText = data.answer;
}
