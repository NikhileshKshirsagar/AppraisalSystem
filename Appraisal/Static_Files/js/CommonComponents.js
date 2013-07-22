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
			 }
			 });
			 $( sliderValueElement ).val( $( sliderElement ).slider( "value" ) );	
	});
	
}

function setSliderValue(sliderElement, sliderValueElement, sliderValue){
	$(function(){
		$( sliderElement ).slider('value', sliderValue);
		$( sliderValueElement ).val( sliderValue );
	});
}