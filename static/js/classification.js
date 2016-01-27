$('form#multi-delete').submit(function () {
	var classificationsList = [];
	$('input.checkthis').each(function () {
		if (this.checked){
			classificationsList.push($(this).val())
		}
	})
	$('form#multi-delete input[name="classification_id"]').val(JSON.stringify(classificationsList));
});