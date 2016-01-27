$('form#multi-delete').submit(function () {
	var brandList = [];
	$('input.checkthis').each(function () {
		if (this.checked){
			brandList.push($(this).val())
		}
	})
	$('form#multi-delete input[name="brand_id"]').val(JSON.stringify(brandList));
});