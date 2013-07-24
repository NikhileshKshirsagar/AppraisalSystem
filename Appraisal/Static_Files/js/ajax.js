function AjaxEvent(sourceElement, destinationElement,searchAttribute, model, successCallback)
{
	var text = $(sourceElement).val();
	if(text != '' && text != null)
	{
		console.log("Inside if " + text);
		$.ajax({
			type : "POST",
			url : "/userSearch/",
			data: {
				'search_txt' : $(sourceElement).val(),
				'searchAttribute' : searchAttribute,
				'model' : model,
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success : successCallback,
			dataType : 'html' 
		});
	}
	else
	{
		$(destinationElement).empty();
	}
}

//function AjaxNonEvent	