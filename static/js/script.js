function dialog() {

  // Declare variables
  var dialogBox = $('.dialog'),
    dialogTrigger = $('.dialog__trigger'),
    dialogClose = $('.dialog__close'),
    overlay = $('.overlay');

  // Open the dialog
  dialogTrigger.on('click', function (e) {
    var dialogId = $(this).data("dialog");
    dialogBox = $('#' + dialogId);
    dialogBox.toggleClass('dialog--active');
    overlay.toggleClass('overlay--active');
    e.stopPropagation();

    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  });

  // Close the dialog - click close button
  dialogClose.on('click', function () {
    dialogBox.removeClass('dialog--active');
    overlay.removeClass('overlay--active');
  });

  // Close the dialog - press escape key // key#27
  $(document).keyup(function (e) {
    if (e.keyCode === 27) {
      dialogBox.removeClass('dialog--active');
      overlay.removeClass('overlay--active');
    }
  });

  // Close the dialog - click outside
  $(document).on('click', function (e) {
    if ($(e.target).is(overlay) === true) {
      dialogBox.removeClass('dialog--active');
      overlay.removeClass('overlay--active');
    }
  });

}

// Run function
$(dialog);

function toggleDropdown(dropdownId) {
  var dropdown = document.getElementById(dropdownId);
  dropdown.classList.toggle('open');
}

let selectedOptionIndex = -1;
const options = ["All Events", "Concerts", "Festivals", "Free Events", "Shows", "Nightlife"];

function toggleSingleDropdown() {
  const dropdown = document.getElementById('dropdown-single');
  dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

function selectOption(index) {
  selectedOptionIndex = index;
  const selectedOption = document.getElementById('selected-option');
  if (selectedOptionIndex == 0) {
    selectedOption.innerHTML = "<i class='fa-solid fa-filter dropdown-icon'></i>Filter";
  } else {
    selectedOption.textContent = options[selectedOptionIndex];
  }
  toggleSingleDropdown();
}


document.addEventListener("DOMContentLoaded", function () {
  const searchButton = document.getElementById("search-button");
  const searchInput = document.getElementById("search-input");
  const locationInput = document.getElementById("location-input");
  const dropdownDate = document.getElementById("dropdown-date");
  const selectedOption = document.getElementById("selected-option");

  searchButton.addEventListener("click", function () {
    performSearch();
  });

  searchInput.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      performSearch();
    }
  });

  locationInput.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      performSearch();
    }
  });

  function toggleDropdown(dropdownId) {
    const dropdown = document.getElementById(dropdownId);
    dropdown.classList.toggle("active");
  }

  function performSearch() {
    var searchTerm = searchInput.value;
    const locationTerm = locationInput.value;
    const selectedDateCheckboxes = document.querySelectorAll("#dropdown-date .dropdown-content input[type='checkbox']:checked");
    const selectedDates = Array.from(selectedDateCheckboxes, checkbox => checkbox.parentElement.textContent.trim());
    var filterValue = selectedOption.textContent;
    if (filterValue != "Filter") {
      searchTerm = filterValue + " " + searchTerm;
    }

    const queryParams = new URLSearchParams({
      query: searchTerm,
      location: locationTerm,
      dates: selectedDates.join(",")
    });

    const currentURL = window.location.protocol + "//" + window.location.host;
    const url = `${currentURL}?${queryParams.toString()}`;
    // console.log("GET request URL:", url);

    window.location.href = url;
  }
});
