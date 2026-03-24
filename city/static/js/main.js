document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("citySearch");
    const reviewCards = document.querySelectorAll(".review-card");
    const noResultsMessage = document.getElementById("noResultsMessage");

    if (searchInput) {
        searchInput.addEventListener("keyup", function () {
            const searchValue = searchInput.value.toLowerCase().trim();
            let matchFound = false;

            reviewCards.forEach(function (card) {
                const cityNameElement = card.querySelector(".city-name");

                if (!cityNameElement) return;

                const cityName = cityNameElement.textContent.toLowerCase();

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

    const createReviewForm = document.getElementById("createReviewForm");

    if (createReviewForm) {
        const draftIdInput = document.getElementById("draft_id");
        const csrfTokenInput = createReviewForm.querySelector('[name="csrfmiddlewaretoken"]');
        let hasSubmitted = false;

        function getCheckedRating() {
            const checked = createReviewForm.querySelector('input[name="rating_score"]:checked');
            return checked ? checked.value : "";
        }

        function autosaveDraft() {
            if (hasSubmitted || !csrfTokenInput) return;

            const cityInput = createReviewForm.querySelector('[name="city_name"]');
            const countryInput = createReviewForm.querySelector('[name="country"]');
            const reviewTextInput = createReviewForm.querySelector('[name="review_text"]');

            const cityName = cityInput ? cityInput.value.trim() : "";
            const country = countryInput ? countryInput.value : "";
            const reviewText = reviewTextInput ? reviewTextInput.value.trim() : "";
            const ratingScore = getCheckedRating();

            // 重點：不要只因為 country 有預設值就存空 draft
            if (!cityName && !reviewText && !ratingScore) {
                return;
            }

            const payload = new URLSearchParams();
            payload.append("csrfmiddlewaretoken", csrfTokenInput.value);
            payload.append("draft_id", draftIdInput ? draftIdInput.value : "");
            payload.append("city_name", cityName);
            payload.append("country", country);
            payload.append("review_text", reviewText);
            payload.append("rating_score", ratingScore);

            fetch("/cityrate/create/autosave/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "X-CSRFToken": csrfTokenInput.value
                },
                body: payload.toString(),
                keepalive: true
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    if (data.draft_id && draftIdInput) {
                        draftIdInput.value = data.draft_id;
                    }
                })
                .catch(function () {
                    // ignore autosave errors
                });
        }

        createReviewForm.addEventListener("submit", function () {
            hasSubmitted = true;
        });

        document.addEventListener("visibilitychange", function () {
            if (document.visibilityState === "hidden") {
                autosaveDraft();
            }
        });

        window.addEventListener("pagehide", autosaveDraft);
    }
});

console.log("City search JS loaded");