$(document).ready(function () {
    if (document.getElementById("select-image-btn")) {
        document.getElementById("select-image-btn").addEventListener('click', function () {
            const btn_submit = document.getElementById("btn_submit_image");
            const fileInput = document.getElementById("chosse_image");
            fileInput.click();
            fileInput.onchange = function () {
                if (fileInput.files.length > 0) {
                    var file = fileInput.files[0];
                    // Thực hiện hành động JavaScript trên tệp đã chọn ở đây
                    // console.log('Bạn đã chọn tệp ' + file.name);
                    btn_submit.click();
                    $('.loading').show();
                }
            }
        })
    }


    // class active khi click vào đổi background
    if (document.getElementsByClassName("wrap-border")) {
        var wrapBorder = document.getElementsByClassName("wrap-border");
        console.log(wrapBorder)
        for (let i = 0; i < wrapBorder.length; i++) {
            wrapBorder[i].onclick = function () {
                for (var j = 0; j < wrapBorder.length; j++) {
                    wrapBorder[j].classList.remove("active");
                }
                wrapBorder[i].classList.add("active");
                // để hiển thị loading trên ảnh khi click
                var loading_img = $('.loading_image');
                loading_img.show()
            }
        }
    }

    // change BG

    if (document.getElementById('btn_img_subject') && document.getElementById('input_img_subject')) {
        // nhấn nút chọn ảnh chủ thể
        var btn_img_subject = document.getElementById('btn_img_subject')
        var input_img_subject = document.getElementById('input_img_subject')
        btn_img_subject.addEventListener('click', function () {
            input_img_subject.click()
        })

        // nhấn nút chọn ảnh nền

        var btn_img_bg = document.getElementById('btn_img_bg')
        var input_img_bg = document.getElementById('input_img_bg')
        btn_img_bg.addEventListener('click', function () {
            input_img_bg.click()
        })


        // hiển thị ảnh khi vừa chọn từ input
        // tag button - input
        var btn_img_subject = document.getElementById('btn_img_subject')
        var btn_img_bg = document.getElementById('btn_img_bg')

        var input_img_subject = document.getElementById('input_img_subject')
        var input_img_bg = document.getElementById('input_img_bg')
        // tag img
        var show_img_subject = document.getElementById("show_img_subject")
        var show_img_bg = document.getElementById("show_img_bg")

        input_img_subject.addEventListener('change', (event) => {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) => {
                show_img_subject.src = e.target.result;
                show_img_subject.style.display = 'block';
            };
            reader.readAsDataURL(file);
        });

        input_img_bg.addEventListener('change', (event) => {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) => {
                show_img_bg.src = e.target.result;
                show_img_bg.style.display = 'block';
            };
            reader.readAsDataURL(file);
        });


    }



    // Blur image
    if(document.getElementById('btn_img_blur')){
        var btnBlur = document.getElementById('btn_img_blur')
        var input_blurBG = document.getElementById('input_img_blur')
        var show_img_blur = document.getElementById('show_img_blur')

        // mở hộp thoại chọn file ảnh khi click vào button
        btnBlur.addEventListener('click', function(e){
            input_blurBG.click()
        });

        input_blurBG.addEventListener('change', (event) => {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) => {
                show_img_blur.src = e.target.result;
                show_img_blur.style.display = 'block';
            };
            reader.readAsDataURL(file);
        });
    }



    // Gray bg image
    if(document.getElementById('btn_img_gray')){
        var btnGray = document.getElementById('btn_img_gray')
        var input_grayBG = document.getElementById('input_img_gray')
        var show_img_gray = document.getElementById('show_img_gray')

        // mở hộp thoại chọn file ảnh khi click vào button
        btnGray.addEventListener('click', function(e){
            input_grayBG.click()
        });

        input_grayBG.addEventListener('change', (event) => {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = (e) => {
                show_img_gray.src = e.target.result;
                show_img_gray.style.display = 'block';
            };
            reader.readAsDataURL(file);
        });
    }
});



// if (document.getElementById("select-image-btn")) {
//     document.getElementById("select-image-btn").addEventListener('click', function () {
//         const btn_submit = document.getElementById("btn_submit_image");
//         const fileInput = document.getElementById("chosse_image");
//         fileInput.click();
//         fileInput.onchange = function () {
//             if (fileInput.files.length > 0) {
//                 var file = fileInput.files[0];
//                 // Thực hiện hành động JavaScript trên tệp đã chọn ở đây
//                 // console.log('Bạn đã chọn tệp ' + file.name);
//                 btn_submit.click();
//             }
//         }
//     })
// }
