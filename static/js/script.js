let currentPlanner = "";

const plannerInfo = {
    home: {
        title: "🏠 Home Interior Planner",
        description: "Create a practical interior budget based on your room and requirements.",
        label: "Rooms & Requirements",
        placeholder: "Example: Living room, bedroom, 2 fans, LED lights, sofa, storage..."
    },

    party: {
        title: "🎉 Party Budget Planner",
        description: "Allocate your party budget across food, decoration and entertainment.",
        label: "Party Details",
        placeholder: "Example: Birthday party, 50 guests, Chennai, simple decoration..."
    },

    jewelry: {
        title: "💎 Jewelry Budget Planner",
        description: "Create a jewelry budget based on your occasion and style.",
        label: "Occasion & Style",
        placeholder: "Example: Wedding, traditional style, gold-tone jewelry..."
    }
};


function openPlanner(type) {

    currentPlanner = type;

    const info = plannerInfo[type];

    document.getElementById("plannerTitle").textContent = info.title;
    document.getElementById("plannerDescription").textContent = info.description;
    document.getElementById("detailsLabel").textContent = info.label;
    document.getElementById("details").placeholder = info.placeholder;

    document.getElementById("plannerSection").classList.remove("hidden");

    document.getElementById("resultBox").classList.add("hidden");

    document.getElementById("plannerSection").scrollIntoView({
        behavior: "smooth"
    });
}


async function generateRecommendation() {

    const budget = Number(document.getElementById("budget").value);
    const details = document.getElementById("details").value.trim();

    if (!budget || budget <= 0) {
        alert("Please enter a valid budget.");
        return;
    }

    if (!details) {
        alert("Please enter your requirements.");
        return;
    }

    const loading = document.getElementById("loading");
    const resultBox = document.getElementById("resultBox");
    const resultText = document.getElementById("resultText");
    const sourceBadge = document.getElementById("sourceBadge");

    loading.classList.remove("hidden");
    resultBox.classList.add("hidden");

    try {

        const response = await fetch("/api/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                planner: currentPlanner,
                budget: budget,
                details: details
            })
        });

        const data = await response.json();

        resultText.textContent = data.recommendation;
        sourceBadge.textContent = data.source;

        resultBox.classList.remove("hidden");

        resultBox.scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {

        resultText.textContent =
            "Something went wrong. Please make sure the server is running.";

        sourceBadge.textContent = "Error";

        resultBox.classList.remove("hidden");

    } finally {

        loading.classList.add("hidden");
    }
}
