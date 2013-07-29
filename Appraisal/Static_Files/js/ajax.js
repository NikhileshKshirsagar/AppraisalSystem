function AjaxEvent(data, destinationElement,searchAttribute, model,successCallback)
{
	//alert(searchAttribute);
	if(searchAttribute != '')
	{
		if( data != '' )
		{
			$.ajax({
				type : "POST",
				url : "/userSearch/",
				data: {
					'search_txt' : data,
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
	else
	{
		$.ajax({
			type : "POST",
			url : "/userInfo/",
			data: {
				'search_txt' : data,
				'model' : model,
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success : successCallback,
			error : function(jqXHR,error, errorThrown){
				console.log(jqXHR);
				console.log(errorThrown);
				console.log(error);
				alert("........................................");
			},
			dataType : 'html' 
		});
		//alert("Ajax executed");
	}
}