<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
/*global opener */
>>>>>>> c25daed (change)
=======
=======
>>>>>>> c5b4b76 (admin static files)
=======
>>>>>>> 76a1a11 (admin static files)
/*global opener */
=======
<<<<<<< HEAD
<<<<<<< HEAD
/*global opener */
=======
>>>>>>> a420006 (production settings)
=======
=======
/*global opener */
>>>>>>> c25daed (change)
>>>>>>> bca57da (change)
>>>>>>> c63776d (admin static files)
<<<<<<< HEAD
>>>>>>> f670750 (admin static files)
=======
=======
=======
/*global opener */
>>>>>>> c25daed (change)
=======
/*global opener */
=======
<<<<<<< HEAD
<<<<<<< HEAD
/*global opener */
=======
>>>>>>> a420006 (production settings)
>>>>>>> 98751f7 (admin static files)
=======
=======
/*global opener */
>>>>>>> c25daed (change)
<<<<<<< HEAD
>>>>>>> b57a7f8 (admin static files)
<<<<<<< HEAD
>>>>>>> c5b4b76 (admin static files)
=======
=======
>>>>>>> bca57da (change)
>>>>>>> c63776d (admin static files)
>>>>>>> f670750 (admin static files)
>>>>>>> 98751f7 (admin static files)
>>>>>>> 76a1a11 (admin static files)
'use strict';
{
    const initData = JSON.parse(document.getElementById('django-admin-popup-response-constants').dataset.popupResponse);
    switch(initData.action) {
    case 'change':
        opener.dismissChangeRelatedObjectPopup(window, initData.value, initData.obj, initData.new_value);
        break;
    case 'delete':
        opener.dismissDeleteRelatedObjectPopup(window, initData.value);
        break;
    default:
        opener.dismissAddRelatedObjectPopup(window, initData.value, initData.obj);
        break;
    }
}
