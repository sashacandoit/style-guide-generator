"use strict";
+function($, window){

	$( "#form-validation" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			inputName: {
				required: true
			},
			inputEmail: {
				required: true,
				email: true
			},
			inputSubject: {
				required: true
			},
			inputMessage: {
				required: true
			},
		}
	});

	$( "#form-validation2" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			inputName2: {
				required: true
			},
			inputEmail2: {
				required: true,
				email: true
			},
			inputSubject2: {
				required: true
			},
			inputMessage2: {
				required: true
			},
		}
	});

	$( "#form-validation3" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			inputName3: {
				required: true
			},
			inputEmail3: {
				required: true,
				email: true
			},
			inputSubject3: {
				required: true
			},
			inputSelect3: {
				required: true
			},
			inputMessage3: {
				required: true
			},
		}
	});

	$( "#form-validation4" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			inputName4: {
				required: true
			},
			inputEmail4: {
				required: true,
				email: true
			},
			inputSubject4: {
				required: true,
			},
			inputMessage4: {
				required: true
			},
		}
	});

	$( "#form-validation5" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			inputName5: {
				required: true
			},
			inputEmail5: {
				required: true,
				email: true
			},
			inputSubject5: {
				required: true,
			},
			inputMessage5: {
				required: true
			},
		}
	});

	$( "#login-form" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			usernameLogin: {
				required: true
			},
			passwordLogin: {
				required: true
			},
		}
	});

	$( "#login-form2" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			usernameLogin2: {
				required: true
			},
			passwordLogin2: {
				required: true
			},
		}
	});

	$( "#login-form3" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			usernameLogin3: {
				required: true
			},
			passwordLogin3: {
				required: true
			},
		}
	});

	$( "#login-form4" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			usernameLogin4: {
				required: true
			},
			passwordLogin4: {
				required: true
			},
		}
	});

	$( "#register-form" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			emailRegister: {
				required: true,
				email: true
			},
			usernameRegister: {
				required: true
			},
			passwordRegister: {
				required: true
			},
			passwordRegisterConfirm: {
				required: true,
				equalTo: '#passwordRegister'
			},
		}
	});

	$( "#register-form2" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			emailRegister2: {
				required: true,
				email: true
			},
			usernameRegister2: {
				required: true
			},
			passwordRegister2: {
				required: true
			},
			passwordRegisterConfirm2: {
				required: true,
				equalTo: '#passwordRegister2'
			},
		}
	});

	$( "#register-form3" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			emailRegister3: {
				required: true,
				email: true
			},
			usernameRegister3: {
				required: true
			},
			passwordRegister3: {
				required: true
			},
			passwordRegisterConfirm3: {
				required: true,
				equalTo: '#passwordRegister3'
			},
		}
	});

	$( "#register-form-widget" ).validate({
		ignore: ':hidden:not(:checkbox)',
		errorElement: 'label',
		errorClass: 'error',
		rules: {
			emailRegisterWidget: {
				required: true,
				email: true
			},
			usernameRegisterWidget: {
				required: true
			},
			passwordRegisterWidget: {
				required: true
			},
		}
	});

	var formValidation = {};

	formValidation.init = function() {

	};	
	window.formValidation = formValidation;

}(jQuery, window);

// initialize app
+function($) {
	formValidation.init();		
}(jQuery);
