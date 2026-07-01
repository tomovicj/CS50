// Copy link by clicking on it
const links = document.querySelectorAll('.copy-link');
links.forEach(link => {
    link.textContent = link.href;
    link.addEventListener('click', event => {
      event.preventDefault();
      navigator.clipboard.writeText(event.target.textContent);
    });
});
