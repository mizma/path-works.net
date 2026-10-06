document.addEventListener("DOMContentLoaded", () => {
    const containers = document.querySelectorAll(
        ".entry-content, .article-content, #featured article"
    );

    containers.forEach((container) => {
        container.querySelectorAll("img").forEach((img) => {
            // Don't wrap an image twice
            if (img.parentElement.matches("a.glightbox")) {
                return;
            }

            const link = document.createElement("a");
            link.href = img.src;
            link.classList.add("glightbox");
            link.dataset.gallery = "site-images";

            img.parentNode.insertBefore(link, img);
            link.appendChild(img);
        });
    });

    GLightbox({
        selector: ".glightbox",
        loop: true,
        keyboardNavigation: true,
        touchNavigation: true,
    });
});
