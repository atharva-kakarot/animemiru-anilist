const nextBtn = document.getElementById("next-airing");
const previousBtn = document.getElementById("previous-airing");
const airingNowDiv = document.getElementById("airing-now-container");

nextBtn.addEventListener("click", function () {
    airingNowDiv.scrollLeft += 400;
});

previousBtn.addEventListener("click", function () {
    airingNowDiv.scrollLeft -= 400;
});

const popNextBtn = document.getElementById("next-popular-anime");
const popPreviousBtn = document.getElementById("previous-popular-anime");
const popDiv = document.getElementById("popular-anime-container");

popNextBtn.addEventListener("click", function () {
    popDiv.scrollLeft += 400;
});

popPreviousBtn.addEventListener("click", function () {
    popDiv.scrollLeft -= 400;
});

const topNextBtn = document.getElementById("next-top-anime");
const topPreviousBtn = document.getElementById("previous-top-anime");
const topDiv = document.getElementById("top-anime-container");

topNextBtn.addEventListener("click", function () {
    topDiv.scrollLeft += 400;
});

topPreviousBtn.addEventListener("click", function () {
    topDiv.scrollLeft -= 400;
});

// const movieNextBtn = document.getElementById("next-anime-movie");
// const moviePreviousBtn = document.getElementById("previous-anime-movie");
// const movieDiv = document.getElementById("anime-movie-container");

// movieNextBtn.addEventListener("click", function () {
//     movieDiv.scrollLeft += 400;
// });

// moviePreviousBtn.addEventListener("click", function () {
//     movieDiv.scrollLeft -= 400;
// });

// document.body.addEventListener("click", function (event) {
//     if (!event.target.closest("#search-button")) {
//         container.innerHTML = "";
//         container.style.display = "none";
//     }
// });

const searchBtn = document.getElementById("search-button");
const container = document.getElementById("container");
const inputBox = document.getElementById("input-box");

function animeContainer(str) {
    const animeCard = document.createElement("div");
    animeCard.classList.add("search-anime-cards");

    const image = document.createElement("img");
    image.classList.add("search-anime-image");
    image.src = str.coverImage.extraLarge;;

    const format = {
        "TV_SHORT": "TV Short",
        "MOVIE": "Movie",
        "SPECIAL": "Special",
        "MUSIC": "Music",
        "MANGA": "Manga",
        "NOVEL": "Novel",
        "ONE_SHOT": "One-shot"
    }

    str.format = format[str.format] || str.format;

    function nullfunc(data) {
        if (!data) {
            return "N/A"
        }
        else {
            return data
        }
    }

    const season = nullfunc(str.season);

    const seasonMap = {
        "WINTER": "Winter",
        "SPRING": "Spring",
        "SUMMER": "Summer",
        "FALL": "Fall",
    };

    const updatedSeasonString = seasonMap[season] || season;

    const details = document.createElement("div");
    details.classList.add("search-anime-details");
    details.innerHTML = `
    <h1 class="search-anime-title">${str.title.romaji}</h1>
    <table style="margin-left: 7px; height: 100px" class="search-anime-details-table">
    <tr>
    <td><i class="fa-solid fa-tv"></i>&nbsp;&nbsp;${nullfunc(str.format)} (${nullfunc(str.episodes)} Episodes)</td>
    </tr>
    <tr>
    <td>
    <div class="search-anime-details-main-div">
    <i class="fa-regular fa-calendar"></i>&nbsp;&nbsp;
    <div class="search-anime-details-div">
    ${updatedSeasonString} ${nullfunc(str.endDate.year)}
    </div>
    </div>
    </td>
    </tr>
    <tr>
    <td><i class="fa-solid fa-star" style="color: gold"></i>&nbsp;&nbsp;${nullfunc(str.averageScore)}%</td>
    </tr>
    </table>`

    animeCard.appendChild(image);
    animeCard.appendChild(details);
    const link = document.createElement("a");
    link.href = `anime/id=${str.id}`;
    link.classList.add("anime-card-links");
    link.appendChild(animeCard);
    container.appendChild(link);
}

searchBtn.addEventListener("click", () => {
    container.style.display = "flex";
    container.style.flexDirection = "column";

    if (inputBox.value === "") {
        container.style.display = "none";
        return false;
    }
    container.innerHTML = "";
    fetch(`api-proxy/${inputBox.value}`)
    .then(handleResponse)
    .then(handleData)
    .catch(handleError)

    function handleResponse(response) {
        return response.json().then(function (json) {
            return response.ok ? json : Promise.reject(json);
        });
    }

    function handleData(data) {
        for (const anime of data.data.Page.media) {
            if (data.data.Page.media.length === 1) {
                container.style.height = "241px";
                animeContainer(anime);
            }
            else {
                container.style.height = "486px";
                animeContainer(anime);
            }
        }
    }

    function handleError(error) {
        alert('Error, check console');
        console.error(error);
    }
});

document.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        searchBtn.click();
    }
});