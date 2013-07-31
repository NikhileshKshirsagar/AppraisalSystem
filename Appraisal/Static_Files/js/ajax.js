function AjaxEvent(jsonData, surl,successCallback,emptyCallback)
{
	jsonData['csrfmiddlewaretoken']= $("input[name=csrfmiddlewaretoken]").val();
	if( jsonData.search_txt != null && jsonData.search_txt != '' )
	{
			$.ajax({
					type : "POST",
					url : surl,
					data: jsonData,
					success : successCallback,
					error : function(jqXHR,error, errorThrown){
						console.log(jqXHR);
						console.log(errorThrown);
						console.log(error);
						alert("........................................");
					},
					dataType : 'html' 
				});
	}
	else
	{
		if(emptyCallback!=null)
			emptyCallback();
	}
}