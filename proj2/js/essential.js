function fill_year_range(id)
{
    var yearSelect = document.getElementById(id);
    var currentYear = new Date().getFullYear();

    // add option for year from current year -> 1900
    for (var year = currentYear; year >= 1900; year--) {
        var option = document.createElement("option");
        option.value = year;
        option.text = year;
        yearSelect.add(option);
    }
}