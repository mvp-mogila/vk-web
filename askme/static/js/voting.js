const items = document.getElementsByClassName('like-section')

for (let item of items) {
    const [like, rating, dislike] = item.children;
    like.addEventListener('click', () => {
        alert('Hello from like!');
    })
    dislike.addEventListener('click', () => {
        alert('Hello from dislike!');
    })
}