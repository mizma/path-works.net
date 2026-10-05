document.addEventListener("DOMContentLoaded", () => {
    const article = document.querySelector(".entry-content");

    if (!article) {
        return;
    }

    const images = article.querySelectorAll("img");

    images.forEach((img) => {
        const link = document.createElement("a");

        link.href = img.src;
        link.classList.add("glightbox");
        link.dataset.gallery = "article";

        img.parentNode.insertBefore(link, img);
        link.appendChild(img);
    });

    GLightbox({
        selector: ".glightbox",
        loop: true,
        keyboardNavigation: true,
        touchNavigation: true,
    });
});
