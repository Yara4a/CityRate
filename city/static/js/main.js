document.addEventListener("DOMContentLoaded", function () {

    // Search reviews by city
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

    // Star rating for create/edit forms
    const starRatingWrappers = document.querySelectorAll(".star-rating");

    starRatingWrappers.forEach(function (wrapper) {
        const labels = wrapper.querySelectorAll(".star");
        const radios = wrapper.querySelectorAll('input[name="rating_score"]');

        if (!labels.length || !radios.length) return;

        function getSelectedValue() {
            const checked = wrapper.querySelector('input[name="rating_score"]:checked');
            return checked ? parseInt(checked.value) : 0;
        }

        function paintStars(value, className) {
            labels.forEach(function (label, index) {
                label.classList.remove("active", "hover");

                const starValue = 5 - index;

                if (starValue <= value) {
                    label.classList.add(className);
                }
            });
        }

        function showSelectedStars() {
            paintStars(getSelectedValue(), "active");
        }

        labels.forEach(function (label, index) {
            const starValue = 5 - index;

            label.addEventListener("mouseenter", function () {
                paintStars(starValue, "hover");
            });

            label.addEventListener("click", function () {
                const radio = wrapper.querySelector(`input[value="${starValue}"]`);
                if (radio) {
                    radio.checked = true;
                }
                showSelectedStars();
            });
        });

        wrapper.addEventListener("mouseleave", function () {
            showSelectedStars();
        });

        showSelectedStars();
    });

    // Autosave draft on create page
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

    // Load cities when country changes
    const countrySelect = document.getElementById("id_country");
    const citySelect = document.getElementById("id_city");

    if (countrySelect && citySelect) {
        countrySelect.addEventListener("change", function () {
            const country = this.value;

            citySelect.innerHTML = '<option value="">Select a city</option>';

            if (!country) {
                return;
            }

            fetch("/cityrate/load-cities/?country=" + encodeURIComponent(country))
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    data.forEach(function (city) {
                        const option = document.createElement("option");
                        option.value = city.id;
                        option.textContent = city.name;
                        citySelect.appendChild(option);
                    });
                })
                .catch(function (error) {
                    console.error("Error loading cities:", error);
                });
        });
    }
});

console.log("CityRate JS loaded");