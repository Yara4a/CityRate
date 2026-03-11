document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("citySearch");
    const reviewCards = document.querySelectorAll(".review-card");

    if (!searchInput) return;

    searchInput.addEventListener("keyup", function () {

        const searchValue = searchInput.value.toLowerCase();

        reviewCards.forEach(function (card) {

            const cityNameElement = card.querySelector(".city-name");

            if (!cityNameElement) return;

            const cityName = cityNameElement.textContent.toLowerCase();

            if (cityName.includes(searchValue)) {
                card.style.display = "";
            } else {
                card.style.display = "none";
            }

        });

    });

});

console.log("City search JS loaded");