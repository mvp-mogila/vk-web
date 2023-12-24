const items = document.getElementsByClassName('like-section')

for (let item of items) {
    const [like, rating, dislike] = item.children;
    like.addEventListener('click', () => {
        rating.innerHTML = Number(rating.innerHTML) + 1;
    })
    dislike.addEventListener('click', () => {
        rating.innerHTML = Number(rating.innerHTML) - 1;
    })
}