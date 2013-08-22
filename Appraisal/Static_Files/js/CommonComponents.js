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
			 	if(ui.value == 0)
			 	{
			 		$('#scaleNarrator').html('');
			 	}
			 	if(ui.value > 0 && ui.value <= 2)
			 	{
			 		$('#scaleNarrator').html('NOVICE');
			 	}
			 	if(ui.value > 2 && ui.value <= 4)
			 	{
			 		$('#scaleNarrator').html('BASIC');
			 	}
			 	if(ui.value > 4 && ui.value <= 6)
			 	{
			 		$('#scaleNarrator').html('COMPETENT');
			 	}
			 	if(ui.value > 6 && ui.value <= 8)
			 	{
			 		$('#scaleNarrator').html('ADVANCED');
			 	}
			 	if(ui.value > 8 && ui.value <= 10)
			 	{
			 		$('#scaleNarrator').html('EXPERT');
			 	}
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
		 dateFormat: 'yy-mm-dd',
		 numberOfMonths: number_of_months,
		 onClose: function( selectedDate ) {
		 $( dateElement2 ).datepicker( "option", "minDate", selectedDate );
		 }
		});
		 $( dateElement2 ).datepicker({
		 defaultDate: "+1w",
		 changeMonth: true,
		 changeYear: true,
		 dateFormat: 'yy-mm-dd',
		 numberOfMonths: 3,
		 onClose: function( selectedDate ) {
		 $( dateElement1 ).datepicker( "option", "maxDate", selectedDate );
		 }
		});
	});
}