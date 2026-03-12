document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("citySearch");
    const reviewCards = document.querySelectorAll(".review-card");
    const noResultsMessage = document.getElementById("noResultsMessage");

    if (!searchInput) return;

    searchInput.addEventListener("keyup", function () {

        const searchValue = searchInput.value.toLowerCase();
        let matchFound = false;

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
        if (noResultsMessage) {
            if (matchFound || searchValue === "") {
                noResultsMessage.style.display = "none";
            } else {
                noResultsMessage.style.display = "block";
            }
        }

    });

});

console.log("City search JS loaded");