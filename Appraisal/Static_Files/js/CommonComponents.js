function LoadSlider(sliderElement, sliderValueElement, maxValue, minValue, defaultValue){
	$(function(){
		 $( sliderElement ).slider({
			 orientation: "horizontal",
			 range: "min",
			 min: minValue,
			 max: maxValue,
			 value: defaultValue,
			 slide: function( event, ui ) {
			 	$( sliderValueElement ).val( ui.value );
			 },
			 change:function(event,ui){
			 	$( sliderValueElement ).val(ui.value );
			 }
			 });
			 $( sliderValueElement ).val(defaultValue);
	});	
}

function setSliderValue(sliderElement, sliderValue){
	$(function(){
		$( sliderElement ).slider('value', sliderValue);
	});
}

function DatePicker(dateElement1, dateElement2, number_of_months)
{
	 $(function() {
		 $( dateElement1 ).datepicker({
		 defaultDate: "+1w",
		 changeMonth: true,
		 changeYear: true,
		 dateFormat: 'dd-mm-yy',
		 numberOfMonths: number_of_months,
		 onClose: function( selectedDate ) {
		 $( dateElement2 ).datepicker( "option", "minDate", selectedDate );
		 }
		});
		 $( dateElement2 ).datepicker({
		 defaultDate: "+1w",
		 changeMonth: true,
		 changeYear: true,
		 dateFormat: 'dd-mm-yy',
		 numberOfMonths: 3,
		 onClose: function( selectedDate ) {
		 $( dateElement1 ).datepicker( "option", "maxDate", selectedDate );
		 }
		});
	});
}