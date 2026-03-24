document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("citySearch");
    const reviewCards = document.querySelectorAll(".review-card");
    const noResultsMessage = document.getElementById("noResultsMessage");

    if (searchInput){
        searchInput.addEventListener("keyup", function () {

<<<<<<< HEAD
    searchInput.addEventListener("keyup", function () {
        const searchValue = searchInput.value.toLowerCase();

        reviewCards.forEach(function (card) {
            const cityNameElement = card.querySelector(".city-name");
=======
            const searchValue = searchInput.value.toLowerCase();
            let matchFound = false;
            reviewCards.forEach(function (card) {

                const cityNameElement = card.querySelector(".city-name");

                if (!cityNameElement) return;

                const cityName = cityNameElement.textContent.toLowerCase();
>>>>>>> origin/Mohammad

                if (cityName.includes(searchValue)) {
                    card.style.display = "";
                    matchFound = true;
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
<<<<<<< HEAD
    });
=======
    }
    const starContainer = document.getElementById("starRating");
    const ratingInput = document.getElementById("id_rating_score");

    if (starContainer && ratingInput) {
        const stars = starContainer.querySelectorAll(".star");
        let selectedRating = parseInt(ratingInput.value) || 0;

        function showStars(value, className) {
            stars.forEach(function (star) {
                const starValue = parseInt(star.dataset.value);
                star.classList.remove("active", "hover");

                if (starValue <= value) {
                    star.classList.add(className);
                }
            });
        }

        function showSelectedRating() {
            showStars(selectedRating, "active");
        }

        stars.forEach(function (star) {
            star.addEventListener("mouseenter", function () {
                const hoverValue = parseInt(star.dataset.value);
                showStars(hoverValue, "hover");
            });

            star.addEventListener("click", function () {
                selectedRating = parseInt(star.dataset.value);
                ratingInput.value = selectedRating;
                showSelectedRating();
            });
        });

        starContainer.addEventListener("mouseleave", function () {
            showSelectedRating();
        });

        showSelectedRating();
    }

>>>>>>> origin/Mohammad
});

console.log("City search JS loaded");