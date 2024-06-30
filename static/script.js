$(document).ready(function() {
    // Store the state of the original list of symptoms
    var originalSymptoms = {};

    // Store the initial state of symptoms
    {% for index, row in symptom_data.iterrows() %}
        originalSymptoms['symptom{{ index }}'] = $('#symptom{{ index }}').prop('checked');
    {% endfor %}

    // Function to update the dropdown options based on the search query
    function updateDropdownOptions() {
        var searchQuery = $('#search').val().toLowerCase();
        var dropdownMenu = $('#searchDropdown');
        dropdownMenu.empty();

        // Filter symptom data based on the search query
        {% for index, row in symptom_data.iterrows() %}
            var symptomName = "{{ row['Symptom'] }}".toLowerCase();
            if (symptomName.includes(searchQuery)) {
                dropdownMenu.append('<a class="dropdown-item" href="#" onclick="selectSymptom(\'' + symptomName + '\')">' + "{{ row['Symptom'] }}" + '</a>');
            }
        {% endfor %}
    }

    // Function to select a symptom and populate the search bar
    window.selectSymptom = function(symptomName) {
        $('#search').val(symptomName);
        $('#searchDropdown').empty();
    }

    // Event listener for search bar input
    $('#search').on('input', function() {
        updateDropdownOptions();
    });

    // Event listener for Clear Search button
    $('#clearSearch').click(function() {
        // Restore the original list of symptoms
        for (var key in originalSymptoms) {
            if (originalSymptoms.hasOwnProperty(key)) {
                $('#' + key).prop('checked', originalSymptoms[key]);
            }
        }
        $('#search').val('');
        $('#searchDropdown').empty();
    });

    // Event listener for Clear Selection button
    $('#clearSelectionButton').click(function() {
        // Uncheck all checkboxes
        $('input[type="checkbox"]').prop('checked', false);
    });
});
