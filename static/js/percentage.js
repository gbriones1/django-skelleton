$('form#multi-delete').submit(function () {
	var percentagesList = [];
	$('input.checkthis').each(function () {
		if (this.checked){
			percentagesList.push($(this).val())
		}
	})
	$('form#multi-delete input[name="percentage_id"]').val(JSON.stringify(percentagesList));
});