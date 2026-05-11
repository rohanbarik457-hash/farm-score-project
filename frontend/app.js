async function calculateScore() {

    const lat = document.getElementById("lat").value;
    const lon = document.getElementById("lon").value;

    const response = await fetch(
        "https://farm-score.onrender.com/calculate",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                lat: lat,
                lon: lon
            })
        }
    );

    const data = await response.json();

    document.getElementById("result").innerHTML =
        "Farm Score: " + data.final_score;
}
