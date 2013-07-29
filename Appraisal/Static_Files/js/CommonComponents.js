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