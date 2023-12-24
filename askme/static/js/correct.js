function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const correctItems = document.getElementsByClassName('not-correct');

for (let correctItem of correctItems) {
    const [, correct] = correctItem.children;
    correct.addEventListener('click', () => {
        const formData = new FormData()
        formData.append('answer_id', correct.dataset.id)

        const request = new Request('/answer/correct', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });
        
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                if (data.error == 1) {
                    alert(data.message);
                } else {
                    var correct_img = $("<img src=\"../static/img/correct.png\" class=\"correct-answer-icon mt-2\">");
                    $('.correct').replaceWith(correct_img);
                }
            });
    });
}
