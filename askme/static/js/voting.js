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

const answerItems = document.getElementsByClassName('answer-like-section')

// for (let answerItem in answerItems) {
//     answerItem.onclick = function (event) {
//         console.log('QQQQ')
//         event.preventDefault();
//         const element = event.target;

//         if (element.nodeName === 'like' || element.nodeName === 'dislike') {
//             const formData = new FormData()
//             formData.append('answer_id', like.dataset.id)

            

//             if (element.nodeName === 'like') {
//                 formData.append('positive', true)
//             } else {
//                 formData.append('positive', false)
//             }

//             const request = new Request('/answer/vote/', {
//                 method: 'POST',
//                 body: formData,
//                 headers: {
//                     'X-CSRFToken': getCookie('csrftoken'),
//                 }
//             });

//             fetch(request)
//                 .then((response) => response.json())
//                 .then((data) => {
//                     rating.innerHTML = data.rating;
//                 });
//         }
//     }
// }

for (let answerItem of answerItems) {
    const [, like, rating, dislike] = answerItem.children;
    console.log(like)
    like.addEventListener('click', () => {
        const formData = new FormData()
        formData.append('answer_id', like.dataset.id)
        formData.append('positive', true)

        const request = new Request('/answer/vote', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                rating.innerHTML = data.rating;
            });
    })
}