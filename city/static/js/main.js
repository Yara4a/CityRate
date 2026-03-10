document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("citySearch");
    const reviewCards = document.querySelectorAll(".review-card");

    if (searchInput) {
        searchInput.addEventListener("keyup", function () {
            const searchValue = searchInput.value.toLowerCase();

            reviewCards.forEach(function (card) {
                const cityName = card.querySelector(".city-name").textContent.toLowerCase();

                if (cityName.includes(searchValue)) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });
    }
});

console.log("Search JS running");