// فعال کردن tooltip‌ها
$(document).ready(function() {
    // فعال کردن tooltip‌های بوت‌استرپ
    $('[data-bs-toggle="tooltip"]').tooltip({
        trigger: 'hover',
        placement: 'top'
    });

    // فعال کردن popover‌ها
    $('[data-bs-toggle="popover"]').popover();

    // تایید قبل از حذف مخاطب
    $('.delete-contact').on('click', function(e) {
        if (!confirm('آیا از حذف این مخاطب مطمئن هستید؟')) {
            e.preventDefault();
        }
    });

    // جستجوی لحظه‌ای مخاطبین
    $('#searchInput').on('keyup', function() {
        const value = $(this).val().toLowerCase();
        $('.contact-list-item').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    // فرمت خودکار شماره تلفن
    $('.phone-input').on('input', function() {
        let value = $(this).val().replace(/\D/g, '');
        if (value.length > 4) {
            value = value.replace(/(\d{4})(\d{3})(\d{4})/, '$1-$2-$3');
        } else if (value.length > 3) {
            value = value.replace(/(\d{4})(\d{3})/, '$1-$2');
        }
        $(this).val(value);
    });

    // نمایش/پنهان کردن رمز عبور
    $('.toggle-password').on('click', function() {
        const input = $(this).siblings('input');
        const icon = $(this).find('i');

        if (input.attr('type') === 'password') {
            input.attr('type', 'text');
            icon.removeClass('bi-eye').addClass('bi-eye-slash');
        } else {
            input.attr('type', 'password');
            icon.removeClass('bi-eye-slash').addClass('bi-eye');
        }
    });
});

// تابع برای نمایش نوتیفیکیشن
function showNotification(message, type = 'success') {
    const alert = $(`
        <div class="alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);

    $('body').append(alert);

    setTimeout(() => {
        alert.alert('close');
    }, 5000);
}

// تابع برای بارگذاری مخاطبین با AJAX
function loadContacts(searchTerm = '') {
    $.ajax({
        url: '/contacts/search/',
        method: 'GET',
        data: { q: searchTerm },
        success: function(data) {
            $('#contactsContainer').html(data);
        },
        error: function() {
            showNotification