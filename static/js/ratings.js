const ratingButtons = document.querySelectorAll('.rating-buttons');

function pressThumb(div, grade) {
    const thumbUp = div.querySelector('.fa-thumbs-up');
    const thumbDown = div.querySelector('.fa-thumbs-down');
    thumbUp.classList.remove('dark-color');
    thumbDown.classList.remove('dark-color');
    if (grade == 1) {
        thumbUp.classList.add('dark-color');
    } else if (grade == -1) {
        thumbDown.classList.add('dark-color');
    }
};


ratingButtons.forEach(button => {
    window.addEventListener('load', () => {
        const rating = parseInt(button.dataset.rating)
        $.ajax({
            url: '/get-rating/?rating=' + rating,
            type: 'GET',
            success: function(data) {
                if (data.grade) {
                    pressThumb(button, data.grade);
                };
            },
            error: function(xhr, status, error) {
                alert(error);
            }
        });
    });
    button.addEventListener('click', event => {
        // Получаем значение рейтинга из data-атрибута кнопки
        const value = parseInt(event.target.dataset.value)
        const rating = parseInt(button.dataset.rating)
        const ratingSum = button.querySelector('.rating-sum');
        // Создаем объект FormData для отправки данных на сервер
        const formData = new FormData();
        // Добавляем id статьи, значение кнопки
        formData.append('rating', rating);
        formData.append('value', value);
        // Отправляем AJAX-Запрос на сервер
        fetch("/rating/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .then(data => {
            // Обновляем значение на кнопке
            ratingSum.textContent = data.rating_sum;
            pressThumb(button, data.grade);
        })
        .catch(error => console.error(error));
    });    
});