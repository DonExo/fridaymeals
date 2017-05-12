$(document).ready(function(){

    // Used to populate meal list depending on the selected category, in profile page
	$('#id_categories').change(function () {
        var category = this.value;
        $.getJSON('/assign_category/', {category: category}, function (data) {
            console.log(data);
            $("#id_meals").empty();
            $.each(data, function (key, value) {
                $('#id_meals').append($('<option>', {
                    value: key,
                    text : value
                }));
            });

        });
    });


    // Used for displaying meal results when you try searching them
	$('#meal_search').keyup(function (){
       var string;
       string = $(this).val();
           $.get('/search_meals/', {meal_title:string}, function (data) {
           $('#searched_meals').html(data).show();
           })
    });


	// Used to remove the added div when you search for meals
	document.addEventListener('mouseup', function (e) {
    var container = document.getElementById('searched_meals');

        if (!container.contains(e.target)) {
            container.style.display = 'none';
            $('#meal_search').val('');
        }
    }.bind(this));


    // Used to hide the flash messages
    setTimeout(function() {
        $('.flash').fadeOut('slow');
    }, 5000);
});